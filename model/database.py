"""Class Database"""

import mysql.connector
from mysql.connector import Error

from param import DATABASE, FIRST_USE_SCRIPT

# TODO : create a conneciton shareable between multiple class


class Database:
    """
    This class represents the database used to store program's data
    """
    def __init__(self, database_name, connection):
        self.database_name = database_name
        self.create(connection)

    def create(self, connection):
        """
        Function for full database creation.
        """
        self.create_database(connection)

        self.create_tables(connection)

    def create_database(self, connection):
        """
        This function creates the database and set it in param.
        """
        cursor = connection.cursor()

        # Database creation
        try:
            query = f"""CREATE DATABASE {self.database_name}"""
            cursor.execute(query)
        except Error as e:
            print(f'Error while connecting to mysql: \n{e}')
            return

        # TODO: Check security advice on that
        # Save database name in param
        with open('./param.py', 'rt') as f:
            params = f.read()
            params = params.replace("''", f"'{self.database_name}'")

        with open('./param.py', 'wt') as f:
            f.write(params)

    def create_tables(self, connection):
        """This function creates table from the script"""
        cursor = connection.cursor()

        with open(FIRST_USE_SCRIPT, 'r') as f:
            data = f.read()
            data = data.replace('mydb', self.database_name)
            try:
                cursor.execute(data, multi=True)
            except Error as e:
                print(f'Error while creating tables: \n{e}')
