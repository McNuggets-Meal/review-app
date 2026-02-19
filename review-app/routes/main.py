"""
Main Routes
Handles home page and other main application pages
"""

import random
from flask import Blueprint, render_template, request
from models.review import get_all_reviews, get_collection_items

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page - displays collection and a featured review"""
    collection = get_collection_items()

    # Pick a random collection entry as the featured review each page load
    featured = random.choice(collection) if collection else None

    return render_template(
        'index.html',
        collection=collection,
        featured=featured
    )

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')
