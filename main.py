"""This file is used to launch the python program"""

from model.database import Database

from model.session import Session
from param import DATABASE


def main():
    """
    Main method of the program
    """
    # We check if the user already created a database

    session = Session()

    try:
        session.connect()

        if not DATABASE:
            database_name = input("Please enter the database name: ")
            Database(database_name, session.connection)

    except Exception:
        session.close()
        raise

    session.close()


if __name__ == '__main__':
    main()
