import getpass
import mysql.connector
from mysql.connector import Error

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
    user = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    db_name = "movies_3950_db"

    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost", user=user, password=password, database=db_name
        )
        print(f"Connected successfully to {db_name}")

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
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()

