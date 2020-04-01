"""User's database"""

import mysql.connector

from param import FIRST_USE_SCRIPT
from typing import List


class Database:
    """
    Database used to store program's data
    """
    def __init__(self, connection, database_name):
        self.database_name = database_name
        self.create_tables(connection)

    def create_tables(self, connection: mysql.connector.connect()):
        """
        User's database table creation.

        :param connection: user's database connection
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

    def insert(self,
               connection: mysql.connector.connect(),
               table: str,
               data: tuple):
        """
        Insert in user's database.

        :param connection: user's database connection
        :param table: table where datas are inserted
        :param data: values inserted
        (column_name=value, column_name2=value2...)

        :return: str
        """

        query = """INSERT INTO %s (%s) VALUES (%s)"""

        columns, values = tuple

        for value in data:
            inserted_data = value.split('=')
            columns += (inserted_data[0],)
            values += (inserted_data[1],)

        cursor = connection.cusor()

        try:
            cursor.execute(query, (table, columns, values))
        except mysql.connector.Error as e:
            print(f"Error while inserting data in table {table}: {e}")
            cursor.close()

        connection.commit()

        cursor.close()
