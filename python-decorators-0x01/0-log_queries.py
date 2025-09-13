#!/usr/bin/python3
import functools
from datetime import datetime
from seed import connect_to_prodev  # reuse your DB connection function

def log_queries(func):
    """Decorator to log SQL queries with timestamp before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0] if args else kwargs.get("query", None)
        if query:
            print(f"[{datetime.now()}] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def execute_query(query):
    """Executes a SQL query on ALX_prodev database"""
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


if __name__ == "__main__":
    rows = execute_query("SELECT * FROM user_data LIMIT 3;")
    print(rows)
