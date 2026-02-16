"""
Main Flask Application
Movie & Game Review PWA
"""

from flask import Flask, render_template, session
import config
from routes.auth import auth_bp
from routes.reviews import reviews_bp
from routes.main import main_bp
from middleware.csrf import get_csrf_token

# Create Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(config)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(reviews_bp, url_prefix='/reviews')

# Make csrf_token available to all templates
@app.context_processor
def inject_csrf_token():
    """Make CSRF token available in all templates"""
    return dict(csrf_token=get_csrf_token())

# Set security headers
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    for header, value in config.SECURITY_HEADERS.items():
        response.headers[header] = value
    return response

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    """403 error handler"""
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('errors/500.html'), 500

# Template filters
@app.template_filter('star_rating')
def star_rating(rating):
    """Convert numeric rating to star symbols"""
    full_stars = '★' * rating
    empty_stars = '☆' * (5 - rating)
    return full_stars + empty_stars

@app.template_filter('truncate_text')
def truncate_text(text, length=150):
    """Truncate text to specified length"""
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + '...'

@app.template_filter('format_date')
def format_date(date_string):
    """Format date string for display"""
    from datetime import datetime
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return date.strftime('%B %d, %Y')
    except:
        return date_string

if __name__ == '__main__':
    print("=" * 60)
    print("Movie & Game Review PWA")
    print("=" * 60)
    print(f"Database: {config.DATABASE_PATH}")
    print(f"Server starting at: http://localhost:5000")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
