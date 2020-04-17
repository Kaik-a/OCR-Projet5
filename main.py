"""Main program file. To launch first."""

from typing import Dict, List

from categories_manager import CategoryManager
from database import Database
from param import DATABASE, GIVEN_CATEGORIES
from products_manager import ProductManager
from session import Session
from stores_manager import StoreManager


def main():
    """
    Main method of the program
    """
    global DATABASE
    category_manager = CategoryManager()
    product_manager = ProductManager()
    store_manager = StoreManager()
    session = Session()

    try:
        session.connect()

        while 1:
            print("You must have already created your database in order to use "
                  "this application, if not please refer to README to have "
                  "some help.\n")
            if not DATABASE:
                while 1:
                    database_name = input("Please enter the database name: ")

                    if session.database_exists(database_name):
                        database = Database(session, database_name)
                        session.close()
                        session = Session()
                        database.session = session
                        try:
                            session.connect()
                            database.populate(category_manager,
                                              product_manager,
                                              store_manager)
                            DATABASE = database_name
                            break
                        except Exception:
                            session.close()
                            raise
                    else:
                        print(f"You entered {database_name} but it was not "
                              "found in mysql. Please check. \n")

            answer = input(f"We found the following database: {DATABASE}, "
                           f"do you want to use it ? Y or N: ")
            if answer.upper() == 'Y':
                break
            elif answer.upper() == 'N':
                DATABASE = ''
                continue
            else:
                print(f"You entered {answer}, please unswer Y or N. \n")
                continue

        while 1:
            choice: str = input(f"Tapez le numéro de la commande à réaliser: \n"
                                f"1 - Quel aliment souhaitez-vous "
                                f"remplacer ? \n "
                                f"2 - Retrouver mes aliments substitués. \n"
                                f"3 - Quitter")

            if choice == 1:
                categories: Dict = {}
                i = 1
                for category in GIVEN_CATEGORIES:
                    categories[i] = category
                    i += 1
                category_choice = input(categories)
                products: List = product_manager.get_bad_products(
                                     category=categories[category_choice],
                                     session=session
                                 )
                product_dict: Dict = {}
                i = 1
                for product in products:
                    product_dict[i] = product
                product_choice = input(product_dict)

                product = product_manager.get_better_product(
                              product_dict[product_choice],
                              session
                          )

                save_choice = input(f"Vous voulez-vous sauvegarder l'aliment"
                                    f"de remplacement {product.product_name_fr}"
                                    f"pour le produit "
                                    f"{product_dict[product_choice]}? Y or N: ")
                if save_choice.upper() == 'Y':
                    product_manager.save_product_replacement(
                        product_dict[product_choice],
                        product.product_name_fr,
                        session
                    )
                    continue
                elif save_choice.upper() == 'N':
                    continue
                else:
                    # TODO: implement wrong entry
                    pass
            elif choice == 2:
                pass
            elif choice == 3:
                print("Au revoir !")
                break
            else:
                # TODO: implement wrong entry
                pass
    except Exception:
        session.close()
        raise

    session.close()


if __name__ == '__main__':
    main()
