#!/usr/bin/python3
import mysql.connector
from seed import connect_to_prodev   # reuse your DB connection utility

class DatabaseConnection:
    """Custom context manager for handling DB connections"""

    def __init__(self):
        """Initialize connection and cursor placeholders"""
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = connect_to_prodev()
        self.cursor = self.connection.cursor()
        return self.cursor   # returned to `as cursor`

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is not None:
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()
        return False   # let exceptions propagate


if __name__ == "__main__":
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print("Query Results:", rows)
