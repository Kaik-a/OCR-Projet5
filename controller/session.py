"""This class allows us to create the connection with mysql"""

from typing import List, Optional

import mysql.connector


class Session:
    """Mysql Session"""
    def __init__(self):
        self.connection: mysql.connector.connection = None
        from param import DATABASE  # pylint: disable=C0415
        self.database: str = DATABASE

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

    def database_exists(self, database_name: str) -> bool:
        """
        Check is database exists in mysql.
        :param database_name: Name of the database to check
        :return: bool
        """
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
        except mysql.connector.Error as error:
            print(f"Error while inserting data: {error}")
            self.connection.rollback()
            cursor.close()
            raise error

        self.connection.commit()

        cursor.close()

    def select(self,
               statement: str,
               filters: Optional[tuple] = None) -> List:
        """
        Select in user's database.
        :param statement: Statement to select
        :param filters: Filters
        :return: List
        """
        cursor = self.connection.cursor()

        try:
            if filters:
                cursor.execute(statement, filters)
            else:
                cursor.execute(statement)
        except mysql.connector.Error as error:
            print(f"Error while retrieving data: {error}")
            cursor.close()
            raise error

        results = cursor.fetchall()

        return results
