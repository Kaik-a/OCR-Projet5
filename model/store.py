"""Class store"""


class Store:
    def __init__(self, name: str, url: str):
        """

        :param name: name of the store
        :param url: url of the store on OpenFoodDacts
        """
        self.id = None
        self.name = name.upper()
        self.url = url

