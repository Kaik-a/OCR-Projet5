"""This class allows us to create the connection with mysql"""

import mysql.connector
from typing import List


class Session:
    def __init__(self):
        self.connection = None
        from param import DATABASE
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

    @staticmethod
    def prepare_insert_statement(table: str,
                                 columns: List) -> str:
        """
        Prepare the insert statement

        :param table: Where to insert datas
        :param columns: Columns of table
        """
        statement = f"""INSERT INTO {table} ({', '.join(columns)}) VALUES ("""

        parameters: List[str] = []

        i = 0
        while i < len(columns):
            parameters.append("%s")
            i += 1

        statement += ', '.join(parameters) + ')'

        return statement

    def insert(self,
               statement: str,
               data: List) -> None:
        """
        Insert in user's database.

        :param statement: statement to insert
        :param data: values inserted
        """
        cursor = self.connection.cursor()

        try:
            cursor.executemany(statement, data)
        except mysql.connector.Error as e:
            print(f"Error while inserting data: {e}")
            self.connection.rollback()
            cursor.close()
            raise e

        self.connection.commit()

        cursor.close()
