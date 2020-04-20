"""Main program file. To launch first."""

from controller.categories_manager import CategoryManager
from controller.products_manager import ProductManager
from controller.session import Session
from controller.stores_manager import StoreManager
from view.user_interface import welcome


def main():
    """
    Main method of the program
    """
    category_manager: CategoryManager = CategoryManager()
    product_manager: ProductManager = ProductManager()
    store_manager: StoreManager = StoreManager()
    session: Session = Session()

    try:
        session.connect()

        session = welcome(category_manager,
                          product_manager,
                          session,
                          store_manager)
    except Exception:
        session.close()
        raise

    session.close()


if __name__ == '__main__':
    main()
