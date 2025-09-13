#!/usr/bin/python3
import functools
from seed import connect_to_prodev   # reuse your DB connection utility

# Simple in-memory cache (dictionary)
_query_cache = {}

def cache_query(func):
    """Decorator to cache results of SQL queries based on query string"""
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        if query in _query_cache:
            print(f"Cache hit for query: {query}")
            return _query_cache[query]

        print(f"Cache miss for query: {query}. Executing against DB...")
        result = func(query, *args, **kwargs)
        _query_cache[query] = result  # store in cache
        return result
    return wrapper


@cache_query
def execute_query(query, limit=None):
    """Execute a query and return results"""
    connection = connect_to_prodev()
    cursor = connection.cursor()
    if limit:
        cursor.execute(query + f" LIMIT {limit}")
    else:
        cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


if __name__ == "__main__":
    q = "SELECT * FROM user_data"
    print(execute_query(q, limit=3))   # First call -> DB
    print(execute_query(q, limit=3))   # Second call -> Cache
