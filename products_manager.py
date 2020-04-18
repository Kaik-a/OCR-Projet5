"""Class ProductManager"""

from dataclasses import dataclass
from requests import get
from typing import Dict, List
from uuid import uuid1

from model.product import Product
from session import Session


@dataclass
class ProductManager:
    """Manager for class Product"""
    table: str = 'Products'

    @staticmethod
    def get_from_openfoodfact(categories: List[str],
                              openfoodfacts_url: str,
                              parameters: Dict) -> List:
        """
        Get all the products from given categories in OpenFoodFact.

        :param categories: List of given categories to filter
        :param openfoodfacts_url: url of Openfoodfacts API
        :param parameters: base_params
        """
        products = []

        for category in categories:
            parameters['tag_0'] = category
            products += get(
                openfoodfacts_url,
                params=parameters
            ).json()['products']

        return products

    @staticmethod
    def convert_to_products(products: List) -> List[Product]:
        """
        Convert list of dictionnaries to list of objects

        :param products: list containing dictionnaries
        """
        product_list: List[Product] = []

        for product in products:
            if (product.get('brands')
                    and product.get('categories_tags')
                    and product.get('nutriscore_grade')
                    and product.get('product_name_fr')
                    and product.get('stores_tags')):
                product_list.append(Product(product.get('brands'),
                                            product.get('categories_tags'),
                                            product.get('nutriscore_grade'),
                                            product.get('packaging_tags'),
                                            product.get('product_name_fr'),
                                            product.get('stores_tags'),
                                            product.get('url')))

        return product_list

    def insert_products_in_database(self,
                                    products: List[Product],
                                    session: Session) -> None:
        """
        Insert products in user's database.

        :param products: List of products to insert in database
        :param session: Session
        """
        columns = sorted([key for key in products[0].__dict__.keys()])

        category_association = []
        store_association = []

        values = []

        for product in products:
            id = str(uuid1())
            values.append((product.brands,
                           str(product.categories_tags),
                           id,
                           product.nutriscore_grade,
                           str(product.packaging_tags),
                           product.product_name_fr,
                           str(product.stores_tags),
                           product.url))
            for category in product.categories_tags:
                category_association.append((id, category))
            for store in product.stores_tags:
                store_association.append((id, store))

        stmt_category_association = """
        INSERT IGNORE INTO Product_Category_Association 
        (product_id, category_id)
        VALUES (%s, (SELECT id FROM Categories WHERE off_id = %s))
        """

        stmt_store_association = """INSERT IGNORE INTO Product_Store_Association 
        (product_id, store_id)
        VALUES (%s, (SELECT id FROM Stores WHERE name = %s))
        """

        stmt = session.prepare_insert_statement(self.table, columns)

        # Insert product values in Products
        session.insert(stmt, values)

        # Insert Product_Category_Association
        session.insert(stmt_category_association, category_association)

        # Insert Product_Store_Association
        session.insert(stmt_store_association, store_association)

    def get_bad_products(self,
                         category: str,
                         session: Session) -> List[Product]:
        """
        Get bad products from given category in user database.

        :param category: Category to filter on
        :param session: Session
        """
        stmt = """
        SELECT 
            p.brands,
            '',
            p.id,
            p.nutriscore_grade,
            p.packaging_tags,
            p.product_name_fr,
            '',
            p.url            
        FROM Product_Category_Association as pca 
        INNER JOIN Products as p 
            ON pca.product_id = p.id
        INNER JOIN Categories as c 
            ON pca.category_id = c.id 
        WHERE 
            pca.category_id = (SELECT id FROM Categories WHERE name = %s)
        AND 'D' <= p.nutriscore_grade
        LIMIT 10
        """

        cursor = session.connection.cursor()

        cursor.execute(stmt, (category,))

        bad_products: List[Product] = [Product(*args) for args in
                                       cursor.fetchall()]

        cursor.close()

        # TODO: Randomize
        return bad_products

    def get_better_product(self,
                           product: Product,
                           session: Session) -> Product:
        """
        Get a better product in replacement.

        :param product: Product to replace.
        :param session: Session.
        :return: None
        """
        stmt = """
        SELECT 
            p.brands,
            '',
            p.id,
            p.nutriscore_grade,
            p.packaging_tags,
            p.product_name_fr,
            '',
            p.url            
        FROM  Products as p 
        INNER JOIN Product_Category_Association as pca 
            ON pca.product_id = p.id
        INNER JOIN Categories as c 
            ON pca.category_id = c.id 
        WHERE 
            pca.category_id = (SELECT Category_id 
                             FROM Product_Category_Association 
                             WHERE Product_id = %s LIMIT 1)
        AND 'B' >= p.nutriscore_grade
        LIMIT 1
        """

        cursor = session.connection.cursor()

        cursor.execute(stmt, (product.id,))

        better_product = cursor.fetchall()

        cursor.close()

        product = Product(*better_product[0])

        return product

    def save_product_replacement(self,
                                 base_product: Product,
                                 replacement_product: Product,
                                 session: Session) -> None:
        """
        Save in database the product substitution.

        :param base_product: Product to replace.
        :param replacement_product: Product which replace.
        :param session: Session.
        :return: None
        """
        stmt = """
        INSERT INTO Registered_products 
        VALUES (%s, %s, NOW())
        """

        cursor = session.connection.cursor()

        try:
            cursor.execute(stmt, (base_product, replacement_product))
            print("Substitution correctement enregistrée")
        except Exception as error:
            print(f"Une erreur a été rencontrée: {error}")
            session.connection.rollback()
            cursor.close()
            raise error

        session.connection.commit()

        cursor.close()

    def get_saved_products(self,
                           session: Session) -> List:
        """
        Get all previously saved products.

        :param session: Session
        :return: List[Product]
        """
        stmt = """
        SELECT 
            p.product_name_fr,
            p2.product_name_fr,
            rp.date
        FROM Registered_Products as rp 
        INNER JOIN Products as p
            ON rp.product_tested = p.id
        INNER JOIN Products as p2 
            ON rp.`product substitued` = p2.id        
        """

        cursor = session.connection.cursor()

        cursor.execute(stmt)

        registered = cursor.fetchall()

        return registered

