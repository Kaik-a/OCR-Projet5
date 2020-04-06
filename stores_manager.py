"""Class StoreManager"""

from requests import get
from typing import List

from model.product import Product
from model.store import Store
from session import Session


class StoreManager:
    """Manager of stores"""

    def __init__(self):
        self.table = 'Stores'

    @staticmethod
    def get_from_openfoodfacts(store_url: str):
        """
        Method to get all the stores contained in OpenFoodFacts

        :param store_url: URL of stores on OpenFoodFact
        :return: List
        """
        return get(store_url).json()['tags']

    def insert_in_user_database(self,
                                session: Session,
                                stores: List[Store]):
        """
        Method to put all stores in database

        :param session: Session
        :param stores: list containing all stores on
        OpenFoodFacts
        :return: None
        """
        columns = [key for key in stores[0].__dict__.keys()]

        values = []

        for store in stores:
            values += f'(UUID(), {store.name}, {store.url})'

        session.insert(self.table, columns, values)

    def get_stores_for_product(self,
                               product: Product,
                               session: Session):
        """

        :param product: Product searched store
        :param session: Seession
        :return: List
        """
        pass

    @staticmethod
    def convert_to_store(stores: List):
        """
        Convert list of dictionnaries to list of objects

        :param stores: list containing dictionnaries
        :return: List
        """
        store_list: List[Store] = []

        for store in stores:
            if (store.get('name')
                    and store.get('url')
                    and store.get('products') > 100):
                store_list += Store(store['name'], store['url'])

        return store_list
