#!/usr/bin/python3
import functools
from seed import connect_to_prodev   # reuse your DB connection utility

def with_db_connection(func):
    """Decorator to handle opening and closing database connections automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = connect_to_prodev()
        try:
            # Pass the connection into the wrapped function
            result = func(connection, *args, **kwargs)
            return result
        finally:
            # Ensure the connection is always closed
            connection.close()
    return wrapper


# Example usage
@with_db_connection
def fetch_users(connection, limit=5):
    """Fetch some users from the user_data table"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data LIMIT %s;", (limit,))
    rows = cursor.fetchall()
    cursor.close()
    return rows


if __name__ == "__main__":
    users = fetch_users(limit=3)
    print("Fetched users:", users)
