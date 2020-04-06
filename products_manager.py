"""Class ProductManager"""

from requests import get
from typing import Dict, List

from model.product import Product
from session import Session


class ProductManager:
    """Manager for class Product"""
    def __init__(self):
        self.table = 'Products'

    @staticmethod
    def get_products_by_categories_from_openfoodfact(categories: List,
                                                     openfoodfacts_url: str,
                                                     parameters: Dict):
        """
        Get all the products from given categories in OpenFoodFact.

        :param categories: List of given categories to filter
        :param openfoodfacts_url: url of Openfoodfacts API
        :param parameters: base_params
        :return: List
        """
        products = []

        for category in categories:
            parameters['tag_0'] = category
            products += get(
                openfoodfacts_url,
                params=parameters
            ).json()[products]

        return products

    def insert_products_in_user_database(self,
                                         products: List[Product],
                                         session: Session):
        """
        Insert products in user's database.

        :param products: List of products to insert in database
        :param session: Session
        :return: None
        """
        columns = [key for key in products[0].__dict__.keys()]

        values = []

        for product in products:
            values += (f'(UUID(), '
                       f'{product.product_name_fr}, '
                       f'{product.brands}, '
                       f'{product.nutriscore_grade}, '
                       f'{product.store_tags}, '
                       f'{product.packaging_tags}, '
                       f'{product.allergens_tags}, '
                       f'{product.nutrient_level}, '
                       f'{product.url})')

        session.insert(self.table, columns, values)

    def get_products_by_category_in_user_database(self,
                                                  category: str,
                                                  session: Session):
        """
        Get products from given category in user database.

        :param category: Category to filter on
        :param session: Session
        :return: Dict
        """
        pass

    @staticmethod
    def convert_to_products(products: List):
        """
        Convert list of dictionnaries to list of objects

        :param products: list containing dictionnaries
        :return: List
        """
        product_list: List[Product] = []

        for product in products:
            if (product.get('allergen_tags')
                    and product.get('brands')
                    and product.get('nutrient_level')
                    and product.get('nutriscore_grade')
                    and product.get('packaging_tags')
                    and product.get('product_name_fr')
                    and product.get('store_tags')
                    and product.get('url')):
                product_list += Product(product['allergen_tags'],
                                        product['brand'],
                                        product['nutriscore_grade'],
                                        product['nutrient_level'],
                                        product['packaging_tags'],
                                        product['product_name_fr'],
                                        product['store_tags'],
                                        product['url'])

            return product_list