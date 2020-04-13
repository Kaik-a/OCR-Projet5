"""class CategoryManager"""

from typing import Dict, List
from uuid import uuid1

from requests import get

from model.category import Category
from session import Session


class CategoryManager:
    """Manager for category class"""
    def __init__(self):
        self.table = "Categories"

    @staticmethod
    def get_from_openfoodfacts(categories_url: str) -> Dict:
        """
        Get categories from OpenFoodFacts.

        :param categories_url: URL of categories on OpenFoodFact
        """
        return get(categories_url).json()['tags']

    @staticmethod
    def convert_to_category(categories: List) -> List:
        """
        Convert list of dictionnaries to list of objects

        :param categories: list containing dictionnaries
        """
        category_list: List[Category] = []

        for category in categories:
            if (category.get('name')
                    and category.get('url')
                    and category.get('id')
                    and category.get('products') > 1000):
                category_list.append(Category(name=category['name'],
                                              off_id=category['id'],
                                              url=category['url']))

        return category_list

    def insert_in_user_database(self,
                                categories: List[Category],
                                session: Session) -> None:
        """
        Put categories in user's database

        :param categories: List containing all categories on
        OpenFoodFacts
        :param session: Session
        """
        columns = sorted([key for key in categories[0].__dict__.keys()])

        values = []

        for category in categories:
            values.append((str(uuid1()),
                           category.name,
                           category.off_id,
                           category.url))

        stmt = session.prepare_insert_statement(self.table, columns)

        session.insert(stmt, values)

    def get_categories_information_from_database(self,
                                                 categories: List,
                                                 session: Session) -> List:
        """
        Get categories's information from database.

        :param categories: List of searched category
        :param session: Session
        """
        pass
