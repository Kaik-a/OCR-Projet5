"""User's database"""

import mysql.connector

from param import FIRST_USE_SCRIPT


class Database:
    """
    Database used to store program's data
    """
    def __init__(self, connection, config_database, database_name):
        self.database_name = database_name
        self.config_database = config_database
        self.create(connection)

    def create(self, connection: mysql.connector.connect()):
        """
        Full user's database creation and register in setup database.

        :rtype: None
        """
        self.create_database(connection)

        self.create_tables(connection)

        self.config_database.set_user_database(self.database_name)

    def create_database(self, connection: mysql.connector.connect()):
        """
        Create user's database.

        :rtype: None
        """
        cursor = connection.cursor()

        try:
            query = f"""CREATE DATABASE {self.database_name}"""
            cursor.execute(query)
        except mysql.connector.Error as e:
            print(f'Error while connecting to mysql: \n{e}')

    def create_tables(self, connection: mysql.connector.connect()):
        """
        User's database table creation.

        :return: None
        """
        cursor = connection.cursor()

        with open(FIRST_USE_SCRIPT, 'r') as f:
            data = f.read()
            data = data.replace('mydb', self.database_name)
            try:
                cursor.execute(data, multi=True)
            except mysql.connector.Error as e:
                print(f'Error while creating tables: \n{e}')
