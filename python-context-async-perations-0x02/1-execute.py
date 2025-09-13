#!/usr/bin/python3
import mysql.connector
from seed import connect_to_prodev   # reuse your DB connection utility

class ExecuteQuery:
    """Custom context manager to execute a query with parameters"""

    def __init__(self, query, params=None):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        # Open connection
        self.connection = connect_to_prodev()
        self.cursor = self.connection.cursor()

        # Execute query
        if self.params:
            self.cursor.execute(self.query, self.params)
        else:
            self.cursor.execute(self.query)

        # Fetch results
        self.result = self.cursor.fetchall()
        return self.result   # This will be returned in `as result`

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is not None:
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()
        return False   # Let exceptions propagate if they occur


if __name__ == "__main__":
    query = "SELECT * FROM user_data WHERE age > %s"
    param = (25,)
    with ExecuteQuery(query, param) as result:
        print("Users older than 25:", result)
