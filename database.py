"""User's database"""

from importlib import reload
import mysql.connector

import param
from categories_manager import CategoryManager
from products_manager import ProductManager
from stores_manager import StoreManager


class Database:
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
            raise mysql.connector.Error(msg=f"Database {self.database_name} "
                                            f"not found, please check in mysql")
        cursor.close()

        self.__save_user_database()

    def __save_user_database(self) -> None:
        """
        Save user's database name in file.
        """
        with open('./param.py', 'rt') as file:
            params = file.read()
            params = params.replace("''", f"'{self.database_name}'")

        with open('./param.py', 'wt') as file:
            file.write(params)

        param.DATABASE = self.database_name

        reload(param)

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
        off_cat = category_manager.get_from_openfoodfacts(param.CATEGORIES_JSON)

        off_store = store_manager.get_from_openfoodfacts(param.STORES_JSON)

        off_product = \
            product_manager.get_from_openfoodfact(
                param.GIVEN_CATEGORIES,
                param.SEARCH_URL,
                param.BASE_SEARCH_PARAMS)

        user_cat = category_manager.convert_to_category(off_cat)
        user_store = store_manager.convert_to_store(off_store)
        user_product = product_manager.convert_to_products(off_product)

        category_manager.insert_in_database(user_cat, self.session)
        store_manager.insert_in_database(self.session, user_store)
        product_manager.insert_products_in_database(user_product,
                                                    self.session)
