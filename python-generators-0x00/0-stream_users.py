#!/usr/bin/python3

seed = __import__('seed')


def stream_users():
    connection = seed.connect_to_prodev()

    if connection:

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM user_data;")
        rows = cursor.fetchall()
        num=0
        while num < len(rows):
            yield rows[num]
            num += 1
        cursor.close()
