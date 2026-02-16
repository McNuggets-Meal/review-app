"""
Database Initialization Script
Creates the SQLite database and tables according to schema.sql
"""

import sqlite3
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def initialize_database():
    """Initialize the database with schema"""

    # Check if database already exists
    if os.path.exists(config.DATABASE_PATH):
        response = input(f"Database already exists at {config.DATABASE_PATH}. Overwrite? (yes/no): ")
        if response.lower() != 'yes':
            print("Database initialization cancelled.")
            return
        # Remove existing database
        os.remove(config.DATABASE_PATH)
        print("Existing database removed.")

    # Create database connection
    print(f"Creating database at: {config.DATABASE_PATH}")
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # Read schema from file
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as schema_file:
        schema_sql = schema_file.read()

    # Execute schema
    try:
        cursor.executescript(schema_sql)
        conn.commit()
        print("[OK] Database schema created successfully!")

        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"[OK] Tables created: {[table[0] for table in tables]}")

    except sqlite3.Error as e:
        print(f"[ERROR] Error creating database schema: {e}")
        conn.rollback()
    finally:
        conn.close()

    print(f"\nDatabase initialized successfully!")
    print(f"Location: {config.DATABASE_PATH}")
    print(f"\nNext step: Run seed_data.py to populate with sample data")

if __name__ == "__main__":
    initialize_database()
