"""
Main Routes
Handles home page and other main application pages
"""

from flask import Blueprint, render_template, request
from models.review import get_all_reviews

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page - displays all reviews"""
    # Get filter parameters
    category = request.args.get('category')
    rating = request.args.get('rating')

    # Validate and convert rating if provided
    if rating:
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                rating = None
        except ValueError:
            rating = None

    # Validate category
    if category and category not in ['movie', 'game']:
        category = None

    # Get reviews with filters
    reviews = get_all_reviews(category=category, rating=rating)

    return render_template(
        'index.html',
        reviews=reviews,
        current_category=category,
        current_rating=rating
    )

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')
