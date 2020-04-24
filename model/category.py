"""Class category"""


class Category:  # pylint: disable=R0903
    """Category"""
    def __init__(self, name: str, off_id: str, url: str):
        """

        :param name: name of the category
        :param off_id: id of the category on OpenFoodFacts
        :param url: url of the category on OpenFoodFacts
        """
        self.id = None  # pylint: disable=C0103
        self.name = name.upper()
        self.off_id = off_id
        self.url = url
