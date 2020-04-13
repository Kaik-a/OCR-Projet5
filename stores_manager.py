"""Class StoreManager"""

from requests import get
from typing import List
from uuid import uuid1

from model.product import Product
from model.store import Store
from session import Session


class StoreManager:
    """Manager of stores"""

    def __init__(self):
        self.table = 'Stores'

    @staticmethod
    def get_from_openfoodfacts(store_url: str) -> List:
        """
        Method to get all the stores contained in OpenFoodFacts

        :param store_url: URL of stores on OpenFoodFact
        """
        return get(store_url).json()['tags']

    @staticmethod
    def convert_to_store(stores: List) -> List:
        """
        Convert list of dictionnaries to list of objects

        :param stores: list containing dictionnaries
        """
        store_list: List[Store] = []

        for store in stores:
            if (store.get('name')
                    and store.get('url')
                    and store.get('products') > 100):
                store_list.append(Store(store['name'], store['url']))

        return store_list

    def insert_in_user_database(self,
                                session: Session,
                                stores: List[Store]) -> None:
        """
        Method to put all stores in database

        :param session: Session
        :param stores: list containing all stores on
        OpenFoodFacts
        """
        columns = sorted([key for key in stores[0].__dict__.keys()])

        values = []

        for store in stores:
            values.append((str(uuid1()), store.name, store.url))

        stmt = session.prepare_insert_statement(self.table, columns)

        session.insert(stmt, values)

    def get_stores_for_product(self,
                               product: Product,
                               session: Session) -> List:
        """

        :param product: Product searched store
        :param session: Seession
        """
        pass

