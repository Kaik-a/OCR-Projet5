"""Module containing all user interface."""

from typing import Callable, Dict, List

from categories_manager import CategoryManager
from database import Database
from param import DATABASE, GIVEN_CATEGORIES
from products_manager import ProductManager
from session import Session
from stores_manager import StoreManager


def define_database(category_manager: CategoryManager,
                    product_manager: ProductManager,
                    session: Session,
                    store_manager: StoreManager) -> None:
    """
    Format user's database to host application's data.

    :param category_manager: CategoryManager
    :param product_manager: ProductManager
    :param session: Session
    :param store_manager: StoreManager
    :return: None
    """
    global DATABASE
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
            print(f"\n"
                  f"Vous avez tapé {database_name} mais celle-ci"
                  f"n'est pas présente dans mysql. Merci de "
                  f"vérifier "
                  f"\n")


def welcome(category_manager: CategoryManager,
            product_manager: ProductManager,
            session: Session,
            store_manager: StoreManager) -> None:
    """
    Function at the beginning of the program.
    It verifies if a database is already set in param.py and if it
    exists.

    :param category_manager: CategoryManager
    :param product_manager: ProductManager
    :param session: Session
    :param store_manager: StoreManager
    :return: None
    """
    global DATABASE

    while 1:
        print("\n"
              "Vous devez avoir déjà créé votre base de données dans mysql"
              "pour utiliser ce programme. Si ce n'est pas le cas et que "
              "vous souhaitez de l'aide, referrez-vous au README à la "
              "racine du projet."
              "\n")

        if not DATABASE:
            define_database(category_manager,
                            product_manager,
                            session,
                            store_manager
                            )

        answer = input(f"\n"
                       f"Nous avons trouvé la base de donéees: {DATABASE}, "
                       f"voulez-vous utiliser celle-ci ? "
                       f"\nO ou N?: \n"
                       f"\n")
        if answer.upper() == 'O':
            break
        elif answer.upper() == 'N':
            DATABASE = ''
            continue
        else:
            print(f"\n"
                  f"Vous avez entré {answer}, merci d'utiliser O ou N "
                  f"\n")
            continue

    return choices(product_manager,
                   session)


def choices(product_manager: ProductManager,
            session: Session) -> None:
    """
    Function to navigate inside the program.

    :param product_manager:
    :param session:
    :return: None
    """
    while 1:
        choice: int = int(input(f"\n"
                                f"Tapez le numéro de la commande à "
                                f"réaliser: \n"
                                f"1 - Quel aliment souhaitez-vous "
                                f"remplacer ? \n"
                                f"2 - Retrouver mes aliments substitués. \n"
                                f"3 - Quitter \n"
                                f"\n"))

        if choice == 1:
            categories: Dict = {}
            i = 0
            for category in GIVEN_CATEGORIES:
                categories[str(i + 1)] = category
                i += 1

            print("Veuillez choisir une categorie: ")
            format_dict(categories)

            category_choice = input()
            products: List = product_manager.get_bad_products(
                category=categories[category_choice],
                session=session
            )
            product_dict: Dict = {}
            i = 0
            for product in products:
                product_dict[i + 1] = product.product_name_fr
                i += 1

            print("Veuillez choisir un produit à substituer: ")
            format_dict(product_dict)

            product_choice = int(input())

            product = product_manager.get_better_product(
                products[product_choice - 1],
                session
            )

            print(f"\n"
                  f"INFORMATION PRODUIT SUBSTITUE \n"
                  f"Nom: {product.product_name_fr} \n"
                  f"Marque: {product.brands} \n"
                  f"Nutriscore: {product.nutriscore_grade} \n"
                  f"Magasin: {''.join(product.stores_tags)} \n"
                  f"url: {product.url} \n"
                  f"Mots-clés: {product.packaging_tags} \n")
            while 1:
                save_choice = input(
                    f"\n"
                    f"Vous voulez-vous sauvegarder l'aliment"
                    f" de remplacement {product.product_name_fr} pour le "
                    f"produit "
                    f"{products[product_choice - 1].product_name_fr}? "
                    f"\nO ou N?: \n"
                    f"\n")

                if save_choice.upper() == 'O':
                    product_manager.save_product_replacement(
                        products[product_choice - 1].id,
                        product.id,
                        session
                    )
                    break
                elif save_choice.upper() == 'N':
                    break

                print(f"\n"
                      f"Vous avez entré {choice} alors que O ou N était "
                      f"attendu. Merci de recommencer."
                      f"\n")

        elif choice == 2:
            registered = product_manager.get_saved_products(session)

            [print(f"\n"
                   f"Le produit {base_product} a été substitué par "
                   f"{replacement_product} le {str(date)}"
                   f"\n")
             for base_product, replacement_product, date in registered]
        elif choice == 3:
            print("Au revoir !")
            return
        else:
            print(f"\n"
                  f"Vous avez entré {choice} alors qu'un chiffre entre 1"
                  f" et 3 était attendu. Merci de recommencer."
                  f"\n")


def format_dict(dictionnary: Dict):
    for key, value in dictionnary.items():
        print(key, '-', value)
    print("\n")


