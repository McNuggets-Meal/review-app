"""
User Model
Handles user-related database operations
"""

import sqlite3
from utils.security import hash_password, verify_password
import config

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
    return conn

def create_user(username, email, password):
    """
    Create a new user

    Args:
        username (str): Username
        email (str): Email address
        password (str): Plain text password (will be hashed)

    Returns:
        int: User ID if successful, None if failed
    """
    try:
        password_hash = hash_password(password)
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        # Username or email already exists
        return None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def get_user_by_username(username):
    """
    Retrieve user by username

    Args:
        username (str): Username to search for

    Returns:
        dict: User data or None if not found
    """
    try:
        conn = get_db_connection()
        user = conn.execute(
            "SELECT id, username, email, password_hash, created_at FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user:
            return dict(user)
        return None
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None

def get_user_by_email(email):
    """
    Retrieve user by email

    Args:
        email (str): Email to search for

    Returns:
        dict: User data or None if not found
    """
    try:
        conn = get_db_connection()
        user = conn.execute(
            "SELECT id, username, email, password_hash, created_at FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        conn.close()

        if user:
            return dict(user)
        return None
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None

def get_user_by_id(user_id):
    """
    Retrieve user by ID

    Args:
        user_id (int): User ID

    Returns:
        dict: User data or None if not found
    """
    try:
        conn = get_db_connection()
        user = conn.execute(
            "SELECT id, username, email, created_at FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        conn.close()

        if user:
            return dict(user)
        return None
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None

def verify_user_password(username, password):
    """
    Verify user credentials

    Args:
        username (str): Username
        password (str): Plain text password

    Returns:
        dict: User data if credentials valid, None otherwise
    """
    user = get_user_by_username(username)
    if not user:
        return None

    if verify_password(password, user['password_hash']):
        # Remove password_hash from returned user data
        del user['password_hash']
        return user
    return None
