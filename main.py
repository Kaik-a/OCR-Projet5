"""Main program file. To launch first."""

from model.database import Database

from model.session import Session
from param import DATABASE


def main():
    """
    Main method of the program
    """

    session = Session()

    try:
        session.connect()

        if not DATABASE:
            database_name = input("Please enter the database name: ")
            Database(session.connection, database_name)

    except Exception:
        session.close()
        raise

    session.close()


if __name__ == '__main__':
    main()
