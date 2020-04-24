"""Class product"""

from typing import List


class Product:  # pylint: disable=R0902,R0903
    """Product"""
    def __init__(self, brands: str, categories_tags: List, id: str,
                 # pylint: disable=R0913,W0622
                 nutriscore_grade: str, packaging_tags: str,
                 product_name_fr: str, stores_tags: List, url: str):
        """
        :param brands: brands making the product
        :param categories_tags: categories of the product
        :param id: id of the product
        :param nutriscore_grade: nutriscore grade (A to F)
        :param packaging_tags: packaging materials
        :param product_name_fr: name of the product in french
        :param stores_tags: stores selling the product
        :param url: url of the product on OpenFoodFact
        """
        self.id = id or None  # pylint: disable=C0103
        self.brands = brands.upper()
        self.categories_tags = [category.upper() for
                                category in categories_tags]
        self.nutriscore_grade = nutriscore_grade.upper()
        self.packaging_tags = packaging_tags
        self.product_name_fr = product_name_fr.upper()
        self.stores_tags = [store.upper() for store in stores_tags]
        self.url = url
        import pdb;pdb.set_trace()

    def __repr__(self):
        return(f"\n"
               f"INFORMATION PRODUIT\n"
               f"Nom: {self.product_name_fr} \n"
               f"Marque: {self.brands} \n"
               f"Nutriscore: {self.nutriscore_grade} \n"
               f"Magasin: {''.join(self.stores_tags)} \n"
               f"url: {self.url} \n"
               f"Mots-clés: {self.packaging_tags} \n")
