"""
Review Model
Handles review-related database operations
"""

import sqlite3
from datetime import datetime
import config

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_review(user_id, title, review_text, rating, category):
    """
    Create a new review

    Args:
        user_id (int): ID of user creating review
        title (str): Movie/game title
        review_text (str): Review content
        rating (int): Rating 1-5
        category (str): 'movie' or 'game'

    Returns:
        int: Review ID if successful, None if failed
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO reviews (user_id, title, review_text, rating, category)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, title, review_text, rating, category)
        )
        conn.commit()
        review_id = cursor.lastrowid
        conn.close()
        return review_id
    except Exception as e:
        print(f"Error creating review: {e}")
        return None

def get_all_reviews(category=None, rating=None):
    """
    Get all reviews with optional filters

    Args:
        category (str, optional): Filter by 'movie' or 'game'
        rating (int, optional): Filter by rating

    Returns:
        list: List of review dicts with user information
    """
    try:
        conn = get_db_connection()

        query = """
            SELECT reviews.*, users.username
            FROM reviews
            JOIN users ON reviews.user_id = users.id
            WHERE 1=1
        """
        params = []

        if category:
            query += " AND reviews.category = ?"
            params.append(category)

        if rating:
            query += " AND reviews.rating = ?"
            params.append(rating)

        query += " ORDER BY reviews.review_date DESC"

        reviews = conn.execute(query, params).fetchall()
        conn.close()

        return [dict(review) for review in reviews]
    except Exception as e:
        print(f"Error retrieving reviews: {e}")
        return []

def get_review_by_id(review_id):
    """
    Get a single review by ID

    Args:
        review_id (int): Review ID

    Returns:
        dict: Review data with user information, None if not found
    """
    try:
        conn = get_db_connection()
        review = conn.execute(
            """SELECT reviews.*, users.username
               FROM reviews
               JOIN users ON reviews.user_id = users.id
               WHERE reviews.id = ?""",
            (review_id,)
        ).fetchone()
        conn.close()

        if review:
            return dict(review)
        return None
    except Exception as e:
        print(f"Error retrieving review: {e}")
        return None

def get_reviews_by_user_id(user_id):
    """
    Get all reviews by a specific user

    Args:
        user_id (int): User ID

    Returns:
        list: List of review dicts
    """
    try:
        conn = get_db_connection()
        reviews = conn.execute(
            """SELECT * FROM reviews
               WHERE user_id = ?
               ORDER BY review_date DESC""",
            (user_id,)
        ).fetchall()
        conn.close()

        return [dict(review) for review in reviews]
    except Exception as e:
        print(f"Error retrieving user reviews: {e}")
        return []

def update_review(review_id, title, review_text, rating, category):
    """
    Update an existing review

    Args:
        review_id (int): Review ID
        title (str): Updated title
        review_text (str): Updated review text
        rating (int): Updated rating
        category (str): Updated category

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """UPDATE reviews
               SET title = ?, review_text = ?, rating = ?, category = ?, updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (title, review_text, rating, category, review_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        print(f"Error updating review: {e}")
        return False

def delete_review(review_id):
    """
    Delete a review

    Args:
        review_id (int): Review ID

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        print(f"Error deleting review: {e}")
        return False

def check_review_ownership(review_id, user_id):
    """
    Check if a user owns a specific review

    Args:
        review_id (int): Review ID
        user_id (int): User ID

    Returns:
        bool: True if user owns review, False otherwise
    """
    review = get_review_by_id(review_id)
    if not review:
        return False
    return review['user_id'] == user_id
