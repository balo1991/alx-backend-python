#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import csv
import uuid
from dotenv import load_dotenv
import os
load_dotenv()


def connect_db():
    """Connect to MySQL server (no DB selected)."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),          # adjust if needed
            password=os.getenv("DB_PASSWORD")       # adjust if needed
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created successfully (or already exists)")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),          # adjust if needed
            password=os.getenv("DB_PASSWORD"),       # adjust if needed
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """Create user_data table if it does not exist."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    );
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    """Insert rows from CSV into user_data table if not already present."""
    cursor = connection.cursor()
    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row.get("user_id") or str(uuid.uuid4())
            name = row["name"]
            email = row["email"]
            age = row["age"]

            cursor.execute(
                "SELECT user_id FROM user_data WHERE user_id = %s;",
                (user_id,)
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);",
                    (user_id, name, email, age)
                )
    connection.commit()
    cursor.close()


def stream_rows(connection):
    """Generator that yields rows from user_data table one by one."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    for row in cursor:
        yield row
    cursor.close()





