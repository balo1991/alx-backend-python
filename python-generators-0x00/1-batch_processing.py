#!/usr/bin/python3

seed = __import__('seed')

def stream_users_in_batches(connection, batch_size=10):

    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    
def batch_processing(connection, batch_size=10):
    for batch in stream_users_in_batches(connection, batch_size):  # loop 2
        yield [user for user in batch if int(user["age"]) > 25]   # comprehension (loop 3)