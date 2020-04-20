"""Class store"""


class Store:  # pylint: disable=R0903
    """Store"""
    def __init__(self, name: str, url: str):
        """

        :param name: name of the store
        :param url: url of the store on OpenFoodDacts
        """
        self.id = None  # pylint: disable=C0103
        self.name = name.upper()
        self.url = url
