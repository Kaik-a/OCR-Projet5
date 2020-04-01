"""Main program file. To launch first."""

from database import Database

from session import Session
from param import DATABASE


def main():
    """
    Main method of the program
    """

    session = Session()

    try:
        session.connect()
        
        if not DATABASE:
            while 1:
                database_name = input("Please enter the database name: ")
                validation = input(f"You typed {database_name}, is it ok? \n"
                                   f"Y / N ")
                validation = validation.upper()
                if validation == 'Y':
                    Database(session, database_name)
                    break
                elif validation != 'N':
                    print(f"You entered {validation}, please type Y or N.")
                    continue
    except Exception:
        session.close()
        raise

    session.close()


if __name__ == '__main__':
    main()
