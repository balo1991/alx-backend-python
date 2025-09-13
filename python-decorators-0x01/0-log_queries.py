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