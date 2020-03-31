"""Main program file. To launch first."""

from model.database import Database

from model.session import Session
from param import ConfigDatabase


def main():
    """
    Main method of the program
    """

    session = Session()

    try:
        session.connect()

        config_database = ConfigDatabase(session.connection)

        # We check if the user already created a database
        user_database = config_database.get_user_database()

        if not user_database:
            database_name = input("Please enter the database name: ")
            Database(session.connection, config_database, database_name)

    except Exception:
        session.close()
        raise

    session.close()


if __name__ == '__main__':
    main()
