"""This class allows us to create the connection with mysql"""

from getpass import getpass
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
        while 1:
            connect_to: str = f"{self.database}" if self.database else 'MySQL'
            user = input(f"Veuillez renseigner l'utilisateur pour se connecter"
                         f" à {connect_to}, si vous voulez utiliser root, "
                         f"appuyer sur Entrée : \n")
            user = user if user else 'root'
            password = getpass(f"Veuillez renseignez le mot de passe de "
                               f"l'utilisateur {user}, s'il n'y en a pas, "
                               f"appuyez sur Entrée :\n")
            try:
                self.connection = mysql.connector.connect(
                    database=self.database,
                    host='localhost',
                    password=password,
                    user=user
                )
                break
            except mysql.connector.Error as error:
                print(f"Nous avons rencontré une erreur lors de la connexion "
                      f"avec l'utilisateur {user}, veuillez vérifier vos "
                      f"informations. \n {error}")
        user = None
        password = None

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
        Prepare the insert statement.

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
