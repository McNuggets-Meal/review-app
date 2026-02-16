"""
Authentication Routes
Handles user registration, login, and logout
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import create_user, get_user_by_username, get_user_by_email, verify_user_password
from utils.validators import validate_username, validate_email, validate_password
from utils.security import sanitize_input
from middleware.csrf import get_csrf_token, validate_csrf_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        csrf_token = request.form.get('csrf_token', '')

        # Validate CSRF token
        if not validate_csrf_token(csrf_token):
            flash('Invalid request. Please try again.', 'danger')
            return redirect(url_for('auth.register'))

        # Validate inputs
        valid, error = validate_username(username)
        if not valid:
            flash(error, 'danger')
            return render_template('auth/register.html', csrf_token=get_csrf_token())

        valid, error = validate_email(email)
        if not valid:
            flash(error, 'danger')
            return render_template('auth/register.html', csrf_token=get_csrf_token())

        valid, error = validate_password(password)
        if not valid:
            flash(error, 'danger')
            return render_template('auth/register.html', csrf_token=get_csrf_token())

        # Check password confirmation
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html', csrf_token=get_csrf_token())

        # Sanitize inputs
        username = sanitize_input(username)
        email = sanitize_input(email)

        # Check if username already exists
        if get_user_by_username(username):
            flash('Username already taken. Please choose another.', 'danger')
            return render_template('auth/register.html', csrf_token=get_csrf_token())

        # Check if email already exists
        if get_user_by_email(email):
            flash('An account with this email already exists.', 'danger')
            return render_template('auth/register.html', csrf_token=get_csrf_token())

        # Create user
        user_id = create_user(username, email, password)
        if user_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'danger')
            return render_template('auth/register.html', csrf_token=get_csrf_token())

    # GET request - show registration form
    return render_template('auth/register.html', csrf_token=get_csrf_token())

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        csrf_token = request.form.get('csrf_token', '')

        # Validate CSRF token
        if not validate_csrf_token(csrf_token):
            flash('Invalid request. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        # Check for empty fields
        if not username or not password:
            flash('Please provide both username and password.', 'danger')
            return render_template('auth/login.html', csrf_token=get_csrf_token())

        # Verify credentials
        user = verify_user_password(username, password)
        if user:
            # Create session
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True

            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('main.index'))
        else:
            # Generic error message (security best practice)
            flash('Invalid username or password.', 'danger')
            return render_template('auth/login.html', csrf_token=get_csrf_token())

    # GET request - show login form
    return render_template('auth/login.html', csrf_token=get_csrf_token())

@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
