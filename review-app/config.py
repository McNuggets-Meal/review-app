"""
Configuration file for the Review App
Contains all application settings including security configurations
"""

import os
from datetime import timedelta

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for session signing (MUST be changed in production!)
# In production, set this as an environment variable
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2026'

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, 'reviews_app.db')

# Session configuration
SESSION_COOKIE_NAME = 'review_app_session'
SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access (XSS protection)
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_COOKIE_SECURE = False  # Set to True in production (HTTPS only)
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)  # Session expires after 24 hours

# Security headers
SECURITY_HEADERS = {
    'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;",
    'X-Frame-Options': 'SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'  # HTTPS only
}

# Bcrypt configuration
BCRYPT_LOG_ROUNDS = 12  # Number of hashing rounds (higher = more secure but slower)

# Application settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max request size
