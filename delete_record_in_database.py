"""
Use Python to execute feature queries from the sql_features folder.
"""

# Imports from Python Standard Library
import sqlite3
import os
import pathlib

# Import local modules
from utils_logger import logger


def execute_sql_file(connection, file_path) -> None:
    """
    Executes a SQL file using the provided SQLite connection.

    Args:
        connection (sqlite3.Connection): SQLite connection object.
        file_path (str): Path to the SQL file to be executed.
    """
    try:
        with open(file_path, 'r') as file:
            sql_script: str = file.read()
        with connection:
            connection.executescript(sql_script)
            logger.info(f"Executed: {file_path}")
    except Exception as e:
        logger.error(f"Failed to execute {file_path}: {e}")
        raise


def main() -> None:

    # Log start of feature execution
    logger.info("Starting feature queries execution...")

    # Define path variables
    ROOT_DIR = pathlib.Path(__file__).parent.resolve()
    SQL_FEATURES_FOLDER = ROOT_DIR.joinpath("sql_features")
    DB_PATH = ROOT_DIR.joinpath('project.sqlite3')

    # Ensure the database file exists before attempting to connect
    if not DB_PATH.exists():
        logger.error(f"Database file not found at {DB_PATH}. Ensure the database is created first.")
        return

    # Connect to SQLite database
    try:
        connection = sqlite3.connect(DB_PATH)
        logger.info(f"Connected to database: {DB_PATH}")

        # Execute all SQL files in the sql_features folder
     # for sql_file in sorted(SQL_FEATURES_FOLDER.glob("*.sql")):
      #      execute_sql_file(connection, sql_file)

        execute_sql_file(connection, SQL_FEATURES_FOLDER.joinpath('delete_records.sql') )

        logger.info("Delete execution completed successfully.")
    except Exception as e:
        logger.error(f"Error during feature queries execution: {e}")
    finally:
        connection.close()
        logger.info("Database connection closed.")


if __name__ == '__main__':
    main()