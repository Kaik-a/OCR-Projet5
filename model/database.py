"""User's database"""

import mysql.connector

from param import FIRST_USE_SCRIPT


class Database:
    """
    Database used to store program's data
    """
    def __init__(self, connection, database_name):
        self.database_name = database_name
        self.connection = connection

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
