"""Class category"""


class Category:
    def __init__(self, name: str, off_id: str, url: str):
        """

        :param name: name of the category
        :param url: url of the category on OpenFoodFacts
        """
        self.id = None
        self.name = name.upper()
        self.off_id = off_id
        self.url = url
