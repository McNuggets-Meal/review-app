"""
Input Validation Utilities
Validates user inputs according to business rules
"""

import re

def validate_username(username):
    """
    Validate username format and length

    Rules:
    - 3-50 characters
    - Only letters, numbers, and underscores

    Args:
        username (str): Username to validate

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"

    if len(username) < 3:
        return False, "Username must be at least 3 characters"

    if len(username) > 50:
        return False, "Username must be at most 50 characters"

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"

    return True, None

def validate_email(email):
    """
    Validate email format

    Args:
        email (str): Email to validate

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    # Basic email regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_pattern, email):
        return False, "Please enter a valid email address"

    if len(email) > 255:
        return False, "Email is too long"

    return True, None

def validate_password(password):
    """
    Validate password strength

    Rules:
    - At least 8 characters

    Args:
        password (str): Password to validate

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if len(password) > 128:
        return False, "Password is too long"

    return True, None

def validate_rating(rating):
    """
    Validate review rating

    Rules:
    - Must be integer between 1 and 5

    Args:
        rating: Rating value

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        rating_int = int(rating)
    except (ValueError, TypeError):
        return False, "Rating must be a number"

    if rating_int < 1 or rating_int > 5:
        return False, "Rating must be between 1 and 5"

    return True, None

def validate_review_text(text):
    """
    Validate review text length

    Rules:
    - 10-5000 characters

    Args:
        text (str): Review text

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Review text is required"

    text = text.strip()

    if len(text) < 10:
        return False, "Review must be at least 10 characters"

    if len(text) > 5000:
        return False, "Review must be at most 5000 characters"

    return True, None

def validate_title(title):
    """
    Validate review title

    Rules:
    - 1-200 characters

    Args:
        title (str): Title text

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Title is required"

    title = title.strip()

    if len(title) < 1:
        return False, "Title cannot be empty"

    if len(title) > 200:
        return False, "Title must be at most 200 characters"

    return True, None

def validate_category(category):
    """
    Validate review category

    Rules:
    - Must be 'movie' or 'game'

    Args:
        category (str): Category value

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not category:
        return False, "Category is required"

    if category not in ['movie', 'game']:
        return False, "Category must be 'movie' or 'game'"

    return True, None
