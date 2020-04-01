"""This class allows us to create the connection with mysql"""

import mysql.connector

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
