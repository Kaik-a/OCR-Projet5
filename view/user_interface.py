"""Module containing all user interface."""

from typing import Dict, List

from controller.categories_manager import CategoryManager
from controller.database import Database
from controller.products_manager import ProductManager
from controller.session import Session
from controller.stores_manager import StoreManager
from param import (
    DATABASE,
    GIVEN_CATEGORIES,
    SEPARATION
)


def define_database(category_manager: CategoryManager,
                    product_manager: ProductManager,
                    session: Session,
                    store_manager: StoreManager) -> Session:
    """
    Format user's database to host application's data.

    :param category_manager: CategoryManager
    :param product_manager: ProductManager
    :param session: Session
    :param store_manager: StoreManager
    :return: Session
    """
    global DATABASE  # pylint: disable=W0603
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

                return session
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
            store_manager: StoreManager) -> Session:
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
    global DATABASE  # pylint: disable=W0603

    while 1:
        print("\n"
              "Vous devez avoir déjà créé votre base de données dans mysql"
              "pour utiliser ce programme. Si ce n'est pas le cas et que "
              "vous souhaitez de l'aide, referrez-vous au README à la "
              "racine du projet."
              "\n")

        if not DATABASE:
            new_session = define_database(category_manager,
                                          product_manager,
                                          session,
                                          store_manager
                                          )

            return navigate(product_manager,
                            new_session)

        answer = input(f"\n"
                       f"Nous avons trouvé la base de donéees: {DATABASE}, "
                       f"voulez-vous utiliser celle-ci ? "
                       f"\nO ou N?: \n"
                       f"\n")
        if answer.upper() == 'O':  # pylint: disable=R1705
            return navigate(product_manager,
                            session)
        elif answer.upper() == 'N':
            DATABASE = ''
        else:
            print(f"\n"
                  f"Vous avez entré {answer}, merci d'utiliser O ou N "
                  f"\n")


def navigate(product_manager: ProductManager,
             session: Session) -> Session:
    """
    Function to navigate inside the program.

    :param product_manager: ProductManager
    :param session: Session
    :return: Session
    """
    while 1:
        print(SEPARATION)
        choice: int = int(input(f"\n"
                                f"Tapez le numéro de la commande à "
                                f"réaliser: \n"
                                f"1 - Quel aliment souhaitez-vous "
                                f"remplacer ? \n"
                                f"2 - Retrouver mes aliments substitués. \n"
                                f"3 - Quitter \n"
                                f"\n"))

        if choice == 1:
            categories, category_choice = choose_category()

            products: List = product_manager.get_bad_products(
                category=categories[category_choice],
                session=session
            )
            product_choice = choose_product(products)

            product = product_manager.get_better_product(
                products[product_choice - 1],
                session
            )
            print(SEPARATION)
            print(product)

            while 1:
                print(SEPARATION)
                save_choice = input(
                    f"\n"
                    f"Vous voulez-vous sauvegarder l'aliment"
                    f" de remplacement {product.product_name_fr} pour le "
                    f"produit "
                    f"{products[product_choice - 1].product_name_fr}? "
                    f"\nO ou N?: \n"
                    f"\n")

                if save_choice.upper() == 'O':  # pylint: disable=R1723
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
            print(SEPARATION)
            [print(f"\n"  # pylint: disable=W0106
                   f"Le produit {base_product} a été substitué par "
                   f"{replacement_product} le {str(date)}")
             for base_product, replacement_product, date in registered]
        elif choice == 3:
            print("Au revoir !")
            return session
        else:
            print(f"\n"
                  f"Vous avez entré {choice} alors qu'un chiffre entre 1"
                  f" et 3 était attendu. Merci de recommencer."
                  f"\n")


def format_dict(dictionnary: Dict):
    """
    Format dictionnaries and add a blank line after.

    :param dictionnary: Dictionnary to format
    :return: None
    """
    for key, value in dictionnary.items():
        print(key, '-', value)
    print("\n")


def choose_category() -> tuple:
    """
    Choose category from categories available.

    :return: tuple (dict(categories), choice from user)
    """
    categories: Dict = create_dict(GIVEN_CATEGORIES)

    theme = "Veuillez choisir une categorie: "

    return categories, validate_choice(categories, theme)


def choose_product(products) -> int:
    """
    Choose a product from bad product list.

    :param products: List of products
    :return: int
    """
    product_dict = create_dict([product.product_name_fr
                                for product in products])

    theme = "Veuillez choisir un produit à substituer: "

    return validate_choice(product_dict, theme)


def create_dict(list_to_transform: List) -> Dict:
    """
    Transform list to dict with numbers as keys.

    :param list_to_transform: List
    :return: Dict
    """
    output_dict: Dict = {}
    i = 1

    for line in list_to_transform:
        output_dict[i] = line
        i += 1

    return output_dict


def validate_choice(dict_choice: Dict,
                    theme: str) -> int:
    """
    Validate users choice through a dict a return the number of the answer.

    :param dict_choice: Dict containing proposals
    :param theme: sentence to explain dict
    :return: int
    """
    while 1:
        print(SEPARATION)
        print("\n")
        print(theme)
        format_dict(dict_choice)
        choice = input()

        try:
            choice = int(choice)
        except ValueError:
            continue

        if choice in dict_choice.keys():
            return choice
