"""
Review Routes
Handles all review CRUD operations
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from models.review import (
    create_review, get_all_reviews, get_review_by_id,
    get_reviews_by_user_id, update_review, delete_review,
    check_review_ownership, get_reviews_by_title
)
from utils.validators import validate_title, validate_review_text, validate_rating, validate_category
from utils.security import sanitize_input
from middleware.auth_required import login_required
from middleware.csrf import get_csrf_token, validate_csrf_token

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new review"""
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '')
        rating = request.form.get('rating', '')
        review_text = request.form.get('review_text', '').strip()
        csrf_token = request.form.get('csrf_token', '')

        # Validate CSRF token
        if not validate_csrf_token(csrf_token):
            flash('Invalid request. Please try again.', 'danger')
            return redirect(url_for('reviews.create'))

        # Validate inputs
        valid, error = validate_title(title)
        if not valid:
            flash(error, 'danger')
            return render_template('reviews/create.html', csrf_token=get_csrf_token())

        valid, error = validate_category(category)
        if not valid:
            flash(error, 'danger')
            return render_template('reviews/create.html', csrf_token=get_csrf_token())

        valid, error = validate_rating(rating)
        if not valid:
            flash(error, 'danger')
            return render_template('reviews/create.html', csrf_token=get_csrf_token())

        valid, error = validate_review_text(review_text)
        if not valid:
            flash(error, 'danger')
            return render_template('reviews/create.html', csrf_token=get_csrf_token())

        # Sanitize inputs
        title = sanitize_input(title)
        review_text = sanitize_input(review_text)

        # Create review
        review_id = create_review(
            user_id=session['user_id'],
            title=title,
            review_text=review_text,
            rating=int(rating),
            category=category
        )

        if review_id:
            flash('Review posted successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Failed to post review. Please try again.', 'danger')
            return render_template('reviews/create.html', csrf_token=get_csrf_token())

    # GET request - show create form
    return render_template('reviews/create.html', csrf_token=get_csrf_token())

@reviews_bp.route('/<int:review_id>')
def view(review_id):
    """View a single review"""
    review = get_review_by_id(review_id)
    if not review:
        abort(404)

    # Check if current user is the owner
    is_owner = False
    if 'user_id' in session:
        is_owner = review['user_id'] == session['user_id']

    return render_template('reviews/view.html', review=review, is_owner=is_owner)

@reviews_bp.route('/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(review_id):
    """Edit a review"""
    review = get_review_by_id(review_id)
    if not review:
        abort(404)

    # Check ownership
    if not check_review_ownership(review_id, session['user_id']):
        abort(403)

    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '')
        rating = request.form.get('rating', '')
        review_text = request.form.get('review_text', '').strip()
        csrf_token = request.form.get('csrf_token', '')

        # Validate CSRF token
        if not validate_csrf_token(csrf_token):
            flash('Invalid request. Please try again.', 'danger')
            return redirect(url_for('reviews.edit', review_id=review_id))

        # Validate inputs
        valid, error = validate_title(title)
        if not valid:
            flash(error, 'danger')
            return render_template('reviews/edit.html', review=review, csrf_token=get_csrf_token())

        valid, error = validate_category(category)
        if not valid:
            flash(error, 'danger')
            return render_template('reviews/edit.html', review=review, csrf_token=get_csrf_token())

        valid, error = validate_rating(rating)
        if not valid:
            flash(error, 'danger')
            return render_template('reviews/edit.html', review=review, csrf_token=get_csrf_token())

        valid, error = validate_review_text(review_text)
        if not valid:
            flash(error, 'danger')
            return render_template('reviews/edit.html', review=review, csrf_token=get_csrf_token())

        # Sanitize inputs
        title = sanitize_input(title)
        review_text = sanitize_input(review_text)

        # Update review
        success = update_review(
            review_id=review_id,
            title=title,
            review_text=review_text,
            rating=int(rating),
            category=category
        )

        if success:
            flash('Review updated successfully!', 'success')
            return redirect(url_for('reviews.view', review_id=review_id))
        else:
            flash('Failed to update review. Please try again.', 'danger')
            return render_template('reviews/edit.html', review=review, csrf_token=get_csrf_token())

    # GET request - show edit form
    return render_template('reviews/edit.html', review=review, csrf_token=get_csrf_token())

@reviews_bp.route('/<int:review_id>/delete', methods=['POST'])
@login_required
def delete(review_id):
    """Delete a review"""
    csrf_token = request.form.get('csrf_token', '')

    # Validate CSRF token
    if not validate_csrf_token(csrf_token):
        flash('Invalid request. Please try again.', 'danger')
        return redirect(url_for('reviews.my_reviews'))

    review = get_review_by_id(review_id)
    if not review:
        abort(404)

    # Check ownership
    if not check_review_ownership(review_id, session['user_id']):
        abort(403)

    # Delete review
    success = delete_review(review_id)
    if success:
        flash('Review deleted successfully.', 'success')
    else:
        flash('Failed to delete review. Please try again.', 'danger')

    return redirect(url_for('reviews.my_reviews'))

@reviews_bp.route('/title/<path:title>')
def by_title(title):
    """View all reviews for a specific movie/game title"""
    reviews = get_reviews_by_title(title)
    if not reviews:
        abort(404)
    category = reviews[0]['category']
    return render_template('reviews/by_title.html', title=title, reviews=reviews, category=category)


@reviews_bp.route('/my')
@login_required
def my_reviews():
    """View current user's reviews"""
    reviews = get_reviews_by_user_id(session['user_id'])
    return render_template('reviews/my_reviews.html', reviews=reviews, csrf_token=get_csrf_token())
