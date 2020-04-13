"""Class ProductManager"""

from requests import get
from typing import Dict, List
from uuid import uuid1

from model.product import Product
from session import Session


class ProductManager:
    """Manager for class Product"""

    def __init__(self):
        self.table = 'Products'

    @staticmethod
    def get_products_by_categories_from_openfoodfact(categories: List,
                                                     openfoodfacts_url: str,
                                                     parameters: Dict) -> List:
        """
        Get all the products from given categories in OpenFoodFact.

        :param categories: List of given categories to filter
        :param openfoodfacts_url: url of Openfoodfacts API
        :param parameters: base_params
        """
        products = []

        for category in categories:
            parameters['tag_0'] = category
            products += get(
                openfoodfacts_url,
                params=parameters
            ).json()['products']

        return products

    @staticmethod
    def convert_to_products(products: List) -> List[Product]:
        """
        Convert list of dictionnaries to list of objects

        :param products: list containing dictionnaries
        """
        product_list: List[Product] = []

        for product in products:
            if (product.get('brands')
                    and product.get('categories_tags')
                    and product.get('nutriscore_grade')
                    and product.get('product_name_fr')
                    and product.get('stores_tags')):
                product_list.append(Product(product.get('brands'),
                                            product.get('categories_tags'),
                                            product.get('nutriscore_grade'),
                                            product.get('packaging_tags'),
                                            product.get('product_name_fr'),
                                            product.get('stores_tags'),
                                            product.get('url')))

        return product_list

    def insert_products_in_user_database(self,
                                         products: List[Product],
                                         session: Session) -> None:
        """
        Insert products in user's database.

        :param products: List of products to insert in database
        :param session: Session
        """
        columns = sorted([key for key in products[0].__dict__.keys()])

        category_association = []
        store_association = []

        values = []

        for product in products:
            id = str(uuid1())
            values.append((product.brands,
                           str(product.categories_tags),
                           id,
                           product.nutriscore_grade,
                           str(product.packaging_tags),
                           product.product_name_fr,
                           str(product.stores_tags),
                           product.url))
            for category in product.categories_tags:
                category_association.append((id, category))
            for store in product.stores_tags:
                store_association.append((id, store))

        stmt_category_association = """
        INSERT IGNORE INTO Product_Category_Association 
        (product_id, category_id)
        VALUES (%s, (SELECT id FROM Categories WHERE off_id = %s))
        """

        stmt_store_association = """INSERT IGNORE INTO Product_Store_Association 
        (product_id, store_id)
        VALUES (%s, (SELECT id FROM Stores WHERE name = %s))
        """

        stmt = session.prepare_insert_statement(self.table, columns)

        # Insert product values in Products
        session.insert(stmt, values)

        # Insert Product_Category_Association
        session.insert(stmt_category_association, category_association)

        # Insert Product_Store_Association
        session.insert(stmt_store_association, store_association)

    def get_products_by_category_in_user_database(self,
                                                  category: str,
                                                  session: Session) -> Dict:
        """
        Get products from given category in user database.

        :param category: Category to filter on
        :param session: Session
        """
        pass


