"""class CategoryManager"""

from requests import get
from typing import List

from model.category import Category
from session import Session


class CategoryManager:
    """Manager for category class"""
    def __init__(self):
        self.table = "Categories"

    @staticmethod
    def get_from_openfoodfacts(categories_url: str):
        """
        Get categories from OpenFoodFacts.

        :param categories_url: URL of categories on OpenFoodFact
        :return: dict
        """
        return get(categories_url).json()['tags']

    def insert_in_user_database(self,
                                categories: List[Category],
                                session: Session):
        """
        Put categories in user's database

        :param categories: List containing all categories on
        OpenFoodFacts
        :param session: Session
        :return: None
        """
        columns = [key for key in categories[0].__dict__.keys()]

        values = []

        for category in categories:
            values += f'(UUID(), {category.name}, {category.url})'

        session.insert(self.table, columns, values)

    def get_categories_information_from_database(self,
                                                 categories: List,
                                                 session: Session):
        """
        Get categories's information from database.

        :param categories: List of searched category
        :param session: Session
        :return: List
        """
        pass

    @staticmethod
    def convert_to_category(categories: List):
        """
        Convert list of dictionnaries to list of objects

        :param categories: list containing dictionnaries
        :return: List
        """
        category_list: List[Category] = []

        for category in categories:
            if (category.get('name')
                    and category.get('url')
                    and category.get('products') > 1000):
                category_list += Category(category['name'], category['url'])

        return category_list
