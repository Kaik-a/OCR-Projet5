"""User's database"""

import mysql.connector

from param import FIRST_USE_SCRIPT
from session import Session
from typing import List


class Database:
    """
    Database used to store program's data
    """
    def __init__(self, session, database_name):
        self.database_name = database_name
        self.__create_tables(session)

    def __create_tables(self, session):
        """
        User's database table creation.

        :param session: user's database connection
        :return: None
        """
        cursor = session.connection.cursor()

        if session.database_exists(self.database_name):
            with open(FIRST_USE_SCRIPT, 'r') as f:
                data = f.read()
                data = data.replace('mydb', self.database_name)
                try:
                    cursor.execute(data, multi=True)
                except mysql.connector.Error as e:
                    print(f'Error while creating tables: \n{e}')
        else:
            raise mysql.connector.Error(msg=f"Database {self.database_name} "
                                            f"not found, please check in mysql")
        cursor.close()

        self.__save_user_database()

    def __save_user_database(self):
        """
        Save user's database name in file

        :return: None
        """
        with open('./param.py', 'rt') as f:
            params = f.read()
            params = params.replace("''", f"'{self.database_name}'")

        with open('./param.py', 'wt') as f:
            f.write(params)
