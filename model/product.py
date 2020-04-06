""""Class product"""


class Product:
    """
    Product object of OpenFoodFact API
    """
    def __init__(self, allergen_tags, brands, nutriscore_grade, nutrient_level,
                 packaging_tags, product_name_fr, store_tags, url):
        """

        :param allergen_tags: allergens in the product
        :param brands: brands making the product
        :param nutriscore_grade: nutriscore grade (A to F)
        :param nutrient_level: score on different nutrient
        :param packaging_tags: packaging materials
        :param product_name_fr: name of the product in french
        :param store_tags: stores selling the product
        :param url: url of the product on OpenFoodFact
        """
        self.allergens_tags = allergen_tags
        self.brands = brands
        self.nutrient_level = nutrient_level
        self.nutriscore_grade = nutriscore_grade
        self.packaging_tags = packaging_tags
        self.product_name_fr = product_name_fr
        self.store_tags = store_tags
        self.url = url
