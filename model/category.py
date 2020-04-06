"""Class category"""


class Category:
    def __init__(self, name: str, url: str):
        """

        :param name: name of the category
        :param url: url of the category on OpenFoodFacts
        """
        self.name = name
        self.url = url
