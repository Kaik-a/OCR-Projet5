"""Main program file. To launch first."""

import pprint
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
    category_manager: CategoryManager = CategoryManager()
    product_manager: ProductManager = ProductManager()
    store_manager: StoreManager = StoreManager()
    session: Session = Session()
    pp = pprint.PrettyPrinter()

    try:
        session.connect()

        while 1:
            print("Vous devez avoir déjà créé votre base de données dans mysql"
                  "pour utiliser ce programme. Si ce n'est pas le cas et que "
                  "vous souhaitez de l'aide, referrez-vous au README à la "
                  "racine du projet.\n")
            if not DATABASE:
                while 1:
                    database_name: str = input("Entrez le nom de la base de "
                                               "données: \n")

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
                        print(f"Vous avez tapé {database_name} mais celle-ci"
                              f"n'est pas présente dans mysql. Merci de "
                              f"vérifier \n")

            answer = input(f"Nous avons trouvé la base de donéees: {DATABASE}, "
                           f"voulez-vous utiliser celle-ci ? O ou N?: \n")
            if answer.upper() == 'O':
                break
            elif answer.upper() == 'N':
                DATABASE = ''
                continue
            else:
                print(f"Vous avez entré {answer}, merci d'utiliser O ou N \n")
                continue

        while 1:
            # TODO: mettre la demande pour le numéro en constante
            choice: int = int(input(f"Tapez le numéro de la commande à "
                                    f"réaliser: \n"
                                    f"1 - Quel aliment souhaitez-vous "
                                    f"remplacer ? \n"
                                    f"2 - Retrouver mes aliments substitués. \n"
                                    f"3 - Quitter\n"))

            if choice == 1:
                categories: Dict = {}
                i = 0
                for category in GIVEN_CATEGORIES:
                    categories[str(i + 1)] = category
                    i += 1
                for key, value in categories.items():
                    print(key, '-', value)
                category_choice = input()
                products: List = product_manager.get_bad_products(
                                     category=categories[category_choice],
                                     session=session
                                 )
                product_dict: Dict = {}
                i = 0
                for product in products:
                    product_dict[i + 1] = (product.product_name_fr,
                                           product.brands,
                                           product.nutriscore_grade)
                    i += 1
                for key, value in product_dict.items():
                    print(key, '-', value[0], '|', value[1], '|', value[2])

                product_choice = int(input())
                product = product_manager.get_better_product(
                              products[product_choice - 1],
                              session
                          )
                # TODO: Formaliser les informations demandées par OCR
                print(f"{product.product_name_fr} | {product.brands} | "
                      f"{product.nutriscore_grade}")
                save_choice = input(
                    f"Vous voulez-vous sauvegarder l'aliment"
                    f" de remplacement {product.product_name_fr} pour le "
                    f"produit {products[product_choice - 1].product_name_fr}? "
                    f"O ou N?: "
                    f"\n")

                if save_choice.upper() == 'O':
                    product_manager.save_product_replacement(
                        products[product_choice - 1].id,
                        product.id,
                        session
                    )
                    continue
                elif save_choice.upper() == 'N':
                    continue
                else:
                    # TODO: implement wrong entry
                    pass
            elif choice == 2:
                registered = product_manager.get_saved_products(session)

                [print(f"Le produit {base_product} a été substitué par "
                       f"{replacement_product} le {str(date)}")
                 for base_product, replacement_product, date in registered]
            elif choice == 3:
                print("Au revoir !")
                break
            else:
                # TODO: implement wrong entry
                pass
            #break
    except Exception:
        session.close()
        raise

    session.close()


if __name__ == '__main__':
    main()
