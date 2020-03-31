"""This class allows us to create the connection with mysql"""

import mysql.connector


class Session:
    def __init__(self):
        self.connection = None
        self.database = None

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
