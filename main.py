"""Main program file. To launch first."""

from database import Database

from categories_manager import CategoryManager
from param import DATABASE
from products_manager import ProductManager
from session import Session
from stores_manager import StoreManager


def main():
    """
    Main method of the program
    """
    global DATABASE
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
                            category_manager = CategoryManager()
                            product_manager = ProductManager()
                            store_manager = StoreManager()
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
    except Exception:
        session.close()
        raise

    session.close()


if __name__ == '__main__':
    main()
