#!/usr/bin/python3
import mysql.connector
from seed import connect_to_prodev   # reuse your DB connection utility

class DatabaseConnection:
    """Custom context manager for handling DB connections"""

    def __enter__(self):
        self.connection = connect_to_prodev()
        self.cursor = self.connection.cursor()
        return self.cursor   # This will be assigned to the variable after `as`

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            # rollback if an exception occurred, otherwise commit
            if exc_type is not None:
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()
        # Returning False lets exceptions propagate
        return False


if __name__ == "__main__":
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print("Query Results:", rows)
