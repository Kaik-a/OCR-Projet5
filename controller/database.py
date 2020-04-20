"""User's database"""

from typing import Dict, List

import mysql.connector

from controller.categories_manager import CategoryManager
from controller.products_manager import ProductManager
from controller.stores_manager import StoreManager
import param


class Database:  # pylint: disable=R0903
    """
    Database used to store program's data
    """
    def __init__(self, session, database_name):
        self.database_name = database_name
        self.session = session
        self.__create_tables(session)

    def __create_tables(self, session) -> None:
        """
        User's database table creation.

        :param session: user's database connection
        """
        cursor = session.connection.cursor()

        if session.database_exists(self.database_name):
            with open(param.FIRST_USE_SCRIPT, 'r') as file:
                data = file.read()
                data = data.replace('mydb', self.database_name)
                try:
                    cursor.execute(data, multi=True)
                except mysql.connector.Error as error:
                    print(f'Error while creating tables: \n{error}')
        else:
            raise mysql.connector.Error(
                msg=f"Database {self.database_name} "
                    f"not found, please check in mysql")
        cursor.close()

        self.__save_user_database()

    def __save_user_database(self) -> None:
        """
        Save user's database name in file.
        """
        with open(param.__file__, 'rt') as file:
            params = file.read()
            params = params.replace("''", f"'{self.database_name}'")

        with open(param.__file__, 'wt') as file:
            file.write(params)

        param.DATABASE = self.database_name

    def populate(self,
                 category_manager: CategoryManager,
                 product_manager: ProductManager,
                 store_manager: StoreManager) -> None:
        """
        Populate the user database with OpenFoodFacts data.

        :param category_manager: categories from OFF
        :param product_manager: products from OOF
        :param store_manager: stores from OOF
        """
        off_data: Dict = self.__get_all_data(category_manager,
                                             product_manager,
                                             store_manager)

        category_manager.insert_in_database(off_data['Categories'],
                                            self.session)
        store_manager.insert_in_database(self.session,
                                         off_data['Stores'])
        product_manager.insert_products_in_database(off_data['Products'],
                                                    self.session)

    def __get_all_data(self,
                       category_manager: CategoryManager,
                       product_manager: ProductManager,
                       store_manager: StoreManager) -> Dict:
        """
        Get all data needed for the application from OpenFoodFacts.

        :param category_manager: CategoryManager
        :param product_manager: ProductManager
        :param store_manager: StoreManager
        :return: Dict
        """
        off_cat = category_manager.get_from_openfoodfacts(
            param.CATEGORIES_JSON)

        off_store = store_manager.get_from_openfoodfacts(param.STORES_JSON)

        off_product = product_manager.get_from_openfoodfact(
            param.GIVEN_CATEGORIES,
            param.SEARCH_URL,
            param.BASE_SEARCH_PARAMS)

        object_dict: Dict[str, List] = {'Categories': off_cat,
                                        'Products': off_product,
                                        'Stores': off_store}

        return self.__convert_to_objects(category_manager,
                                         object_dict,
                                         product_manager,
                                         store_manager)

    @staticmethod
    def __convert_to_objects(category_manager: CategoryManager,
                             object_dict: Dict,
                             product_manager: ProductManager,
                             store_manager: StoreManager) -> Dict:
        """
        Convert all dict to objects according to the key.

        :param category_manager: CategoryManager
        :param object_dict: Dictionnary containing lines to convert.
        :param product_manager: ProductManager
        :param store_manager: StoreManager
        :return: Dict
        """

        user_cat = category_manager.convert_to_category(
            object_dict['Categories']
        )
        user_product = product_manager.convert_to_products(
            object_dict['Products']
        )
        user_store = store_manager.convert_to_store(
            object_dict['Stores']
        )

        return {'Categories': user_cat,
                'Products': user_product, 'Stores': user_store}
