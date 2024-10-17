import psycopg2
from psycopg2 import sql

# Database connection parameters
DATABASE_URL = "postgresql://postgres:1234@localhost/WildlifeApplicationDatabase"

def create_tables():
    # SQL commands to create the necessary tables
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        hashed_password VARCHAR NOT NULL,
        role VARCHAR(20) DEFAULT ''
    );
    """

    create_sightings_table = """
    CREATE TABLE IF NOT EXISTS sightings (
        id SERIAL PRIMARY KEY,
        species VARCHAR NOT NULL,
        location VARCHAR NOT NULL,
        date DATE NOT NULL,
        time TIME NOT NULL
    );
    """

    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        # Execute the create table commands
        cursor.execute(create_users_table)
        cursor.execute(create_sightings_table)

        # Commit the changes
        connection.commit()

        print("Tables 'users' and 'sightings' created successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the database connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    create_tables()
