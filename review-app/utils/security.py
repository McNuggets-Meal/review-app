"""
Security Utilities
Handles password hashing, CSRF token generation, and input sanitization
"""

import bcrypt
import secrets
import html
from config import BCRYPT_LOG_ROUNDS

def hash_password(password):
    """
    Hash a password using bcrypt

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password (60 characters)
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=BCRYPT_LOG_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password, password_hash):
    """
    Verify a password against its hash using constant-time comparison

    Args:
        password (str): Plain text password to verify
        password_hash (str): Stored password hash

    Returns:
        bool: True if password matches, False otherwise
    """
    password_bytes = password.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)

def generate_csrf_token():
    """
    Generate a cryptographically secure CSRF token

    Returns:
        str: 64-character hexadecimal token
    """
    return secrets.token_hex(32)  # 32 bytes = 64 hex characters

def sanitize_input(text):
    """
    Sanitize user input to prevent XSS attacks
    Converts HTML special characters to HTML entities

    Args:
        text (str): User input text

    Returns:
        str: Sanitized text safe for display
    """
    if text is None:
        return None
    # HTML escape to prevent XSS
    sanitized = html.escape(text)
    # Remove null bytes
    sanitized = sanitized.replace('\x00', '')
    return sanitized.strip()
