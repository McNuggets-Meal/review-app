"""
CSRF Protection Middleware
Generates and validates CSRF tokens
"""

from flask import session, abort
from utils.security import generate_csrf_token
import secrets

def get_csrf_token():
    """
    Get or create CSRF token for the current session

    Returns:
        str: CSRF token
    """
    if 'csrf_token' not in session:
        session['csrf_token'] = generate_csrf_token()
    return session['csrf_token']

def validate_csrf_token(token):
    """
    Validate CSRF token against session token

    Args:
        token (str): Token from form submission

    Returns:
        bool: True if valid, False otherwise
    """
    if 'csrf_token' not in session:
        return False

    if not token:
        return False

    # Use constant-time comparison to prevent timing attacks
    return secrets.compare_digest(token, session['csrf_token'])
