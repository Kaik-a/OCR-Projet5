"""Class Database"""

import mysql.connector
from mysql.connector import Error

from param import FIRST_USE_SCRIPT
# TODO : create a conneciton shareable between multiple class


class Database:
    """
    This class represents the database used to store program's data
    """
    def __init__(self, database_name):
        self.database_name = database_name

    def create_database(self):
        """This function creates the database and set it in param"""
        conn = mysql.connector.connect(host='localhost',
                                       user='root')

        cursor = conn.cursor()

        # Database creation
        try:
            query = f"""CREATE DATABASE {self.database_name}"""
            cursor.execute(query)
        except Error as e:
            print(f'Error while connecting to mysql: \n{e}')
            conn.close()
            return

        conn.close()
        # TODO: Check security advice on that
        # Save database name in param
        with open('./param.py', 'rt') as f:
            params = f.read()
            params = params.replace("''", f"'{self.database_name}'")

        with open('./param.py', 'wt') as f:
            f.write(params)

    def create_tables(self):
        """This function creates table from the script"""
        conn = mysql.connector.connect(database=self.database_name,
                                       host='localhost',
                                       user='root')

        cursor = conn.cursor()

        with open(FIRST_USE_SCRIPT, 'r') as f:
            data = f.read()
            data = data.replace('mydb', self.database_name)
            import pdb; pdb.set_trace()
            cursor.execute(data, multi=True)

        conn.close()

