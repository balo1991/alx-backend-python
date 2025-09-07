#!/usr/bin/python3
seed = __import__('seed')


    
def stream_user_ages():
    """
    Generator that yields user ages one by one from user_data.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for (age,) in cursor:      # ✅ loop 1
        yield int(age)
    cursor.close()
    
def average_age(connection):
    """
    Calculate average age using the generator without loading all rows in memory.
    """
    total = 0
    count = 0
    for age in stream_user_ages():  # ✅ streaming
        total += age
        count += 1
    return total / count if count > 0 else 0

    

