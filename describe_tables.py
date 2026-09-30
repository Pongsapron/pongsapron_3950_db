import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

# Load DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE from .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path, override=True)

TABLES = {
    "movies": """
        CREATE TABLE IF NOT EXISTS movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100),
            release_year YEAR,
            genre VARCHAR(100),
            collection_in_mil INT
        )
    """,
    "reviewers": """
        CREATE TABLE IF NOT EXISTS reviewers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100)
        )
    """,
    "ratings": """
        CREATE TABLE IF NOT EXISTS ratings (
            movie_id INT,
            reviewer_id INT,
            rating DECIMAL(2,1),
            PRIMARY KEY (movie_id, reviewer_id),
            FOREIGN KEY (movie_id) REFERENCES movies(id),
            FOREIGN KEY (reviewer_id) REFERENCES reviewers(id)
        )
    """,
}

def main():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
        )
        print(f"Connected successfully to {os.getenv('DB_DATABASE')}")

        cursor = connection.cursor()

        for name, ddl in TABLES.items():
            cursor.execute(ddl)
            print(f"Table '{name}' created successfully")
        print("All tables created successfully!")
        print("-" * 50)

        for name in TABLES:
            print(f"Describing '{name}' table structure:")
            cursor.execute(f"DESCRIBE {name}")
            for column in cursor.fetchall():
                print(column)
            print("-" * 50)

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()