import sqlite3
from venv import logger
import pandas as pd
import pathlib
import csv

# Define the database file in the current root project directory
db_file = pathlib.Path("project.sqlite3")
ROOT_DIR = pathlib.Path(__file__).parent.resolve()
SQL_CREATE_FOLDER = ROOT_DIR.joinpath("sql_create")
DATA_FOLDER=ROOT_DIR.joinpath("data")
AUTHORS_CSV=DATA_FOLDER.joinpath('authors.csv')
BOOKS_CSV=DATA_FOLDER.joinpath('books.csv')


def execute_create_tables(connection, file_path) -> None:
    """
    Executes a SQL file using the provided SQLite connection.

    Args:
        connection (sqlite3.Connection): SQLite connection object.
        file_path (str): Path to the SQL file to be executed.
    """
    # We know reading from a file can raise exceptions, so we wrap it in a try block
    # For example, the file might not exist, or the file might not be readable
    try:
        with open(file_path, 'r') as file:
            # Read the SQL file into a string
            sql_script: str = file.read()
        with connection:
            # Use the connection as a context manager to execute the SQL script
            connection.executescript(sql_script)
            logger.info(f"Executed: {file_path}")
    except Exception as e:
        logger.error(f"Failed to execute {file_path}: {e}")
        raise

def insert_csv_data(connection, CSV_FILE, table_name):
    cursor=connection.cursor()
    try:
        with open(CSV_FILE) as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header row if it exists
            placeholders = ', '.join(['?'] * len(header))
            

          # Prepare the INSERT statement
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"

          # Insert data row by row
            for row in csv_reader:
                cursor.execute(insert_query, row)
     # Commit changes and close connection
        connection.commit()
        print("Data inserted successfully.")

    except sqlite3.Error as e:
         print("Error loading data", e)



def create_database():
    """Function to create a database. Connecting for the first time
    will create a new database file if it doesn't exist yet.
    Close the connection after creating the database
    to avoid locking the file."""
    try:
        conn = sqlite3.connect(db_file)
        execute_create_tables(conn, SQL_CREATE_FOLDER.joinpath('Create_Tables.sql'))
        insert_csv_data(conn,AUTHORS_CSV,'authors')
        insert_csv_data(conn,BOOKS_CSV, 'books' )
        conn.close()
        print("Database created successfully.")
    except sqlite3.Error as e:
        print("Error creating the database:", e)

def main():
    create_database()

if __name__ == "__main__":
    main()