"""This file is used to launch the python program"""

from model.database import Database
from param import DATABASE


def main():
    """
    Main method of the program
    """
    # We check if the user already created a database
    if not DATABASE:
        database_name = input("Please enter the database name: ")
        new_database = Database(database_name)
        new_database.create_database()
        new_database.create_tables()


if __name__ == '__main__':
    main()
