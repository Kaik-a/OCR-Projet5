""""Class product"""


class Product:
    """
    Product object of OpenFoodFact API
    """
    def __init__(self, brands, categories_tags, id, nutriscore_grade,
                 packaging_tags, product_name_fr, stores_tags, url):
        """
        :param brands: brands making the product
        :param categories_tags: categories of the product
        :param nutriscore_grade: nutriscore grade (A to F)
        :param packaging_tags: packaging materials
        :param product_name_fr: name of the product in french
        :param stores_tags: stores selling the product
        :param url: url of the product on OpenFoodFact
        """
        self.id = id or None
        self.brands = brands.upper()
        self.categories_tags = [category.upper() for
                                category in categories_tags]
        self.nutriscore_grade = nutriscore_grade.upper()
        self.packaging_tags = packaging_tags
        self.product_name_fr = product_name_fr.upper()
        self.stores_tags = [store.upper() for store in stores_tags]
        self.url = url
