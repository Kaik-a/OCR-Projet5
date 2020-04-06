"""This class allows us to create the connection with mysql"""

import mysql.connector
from typing import List

from param import DATABASE


class Session:
    def __init__(self):
        self.connection = None
        self.database = DATABASE

    def connect(self):
        """
        Connect to mysql.

        :return: None
        """
        self.connection = mysql.connector.connect(database=self.database,
                                                  host='localhost',
                                                  user='root')

    def close(self):
        """
        Close mysql connection.

        :return: None
        """
        self.connection.close()

    def database_exists(self, database_name):
        cursor = self.connection.cursor()

        cursor.execute("""show databases""")

        databases = cursor.fetchall()

        for database in databases:
            if database[0] == database_name:
                return True
        return False

    def insert(self,
               table: str,
               columns: List,
               data: List):
        """
        Insert in user's database.

        :param table: table destination
        :param columns: columns of the table
        :param data: values inserted

        :return: str
        """

        query = """INSERT INTO %s (%s) VALUES %s"""

        cursor = self.connection.cusor()

        try:
            cursor.execute(query, (table, ', '.join(columns), ', '.join(data)))
        except mysql.connector.Error as e:
            print(f"Error while inserting data in table {table}: {e}")
            cursor.close()

        self.connection.commit()

        cursor.close()