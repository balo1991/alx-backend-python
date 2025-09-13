#!/usr/bin/python3
import functools

def log_queries(func):
    """Decorator to log SQL queries before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # If query is passed as the first argument, log it
        if args:
            query = args[0]
            print(f"Executing SQL Query: {query}")
        elif "query" in kwargs:
            print(f"Executing SQL Query: {kwargs['query']}")
        return func(*args, **kwargs)
    return wrapper


# Example usage
@log_queries
def execute_query(query, cursor=None):
    """Dummy function that simulates executing a query"""
    if cursor:
        cursor.execute(query)
        return cursor.fetchall()
    return f"Simulated run -> {query}"


if __name__ == "__main__":
    # Simulate execution
    result = execute_query("SELECT * FROM user_data LIMIT 3;")
    print(result)
