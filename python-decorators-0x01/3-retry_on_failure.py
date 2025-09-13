#!/usr/bin/python3
import functools
import time
from seed import connect_to_prodev   # reuse your DB connection utility

def retry_on_failure(retries=3, delay=2):
    """Decorator that retries a function if it raises an exception"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            # If all retries failed, re-raise the last exception
            raise last_exception
        return wrapper
    return decorator


# Example usage
@retry_on_failure(retries=3, delay=1)
def fetch_users(limit=3):
    """Fetch some users from the user_data table"""
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data LIMIT %s;", (limit,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


if __name__ == "__main__":
    try:
        users = fetch_users(limit=3)
        print("Fetched users:", users)
    except Exception as e:
        print("Operation failed after retries:", e)
