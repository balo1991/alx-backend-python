#!/usr/bin/python3

import mysql.connector


def stream_users_in_batches(connection, batch_size=10):
    """
    Generator that fetches rows from user_data in batches.
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    while True:  # loop 1
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()


def batch_processing(connection, batch_size=10):
    """
    Generator that processes batches and yields users over age 25.
    """
    for batch in stream_users_in_batches(connection, batch_size):  # loop 2
        yield [user for user in batch if int(user["age"]) > 25]   # loop 3 (inside comprehension)
