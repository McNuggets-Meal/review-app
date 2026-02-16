// Review Form Enhancements

document.addEventListener('DOMContentLoaded', () => {
    // Star Rating Input
    const starRating = document.getElementById('starRating');
    const ratingInput = document.getElementById('rating');

    if (starRating && ratingInput) {
        const stars = starRating.querySelectorAll('.star');

        // Set initial rating if editing
        const initialRating = starRating.dataset.initialRating;
        if (initialRating) {
            setStarRating(parseInt(initialRating));
        }

        // Click event for each star
        stars.forEach(star => {
            star.addEventListener('click', () => {
                const rating = parseInt(star.dataset.rating);
                setStarRating(rating);
                ratingInput.value = rating;
            });

            star.addEventListener('mouseenter', () => {
                const rating = parseInt(star.dataset.rating);
                highlightStars(rating);
            });
        });

        // Reset to actual rating on mouse leave
        starRating.addEventListener('mouseleave', () => {
            if (ratingInput.value) {
                setStarRating(parseInt(ratingInput.value));
            } else {
                clearStars();
            }
        });

        function setStarRating(rating) {
            stars.forEach((star, index) => {
                if (index < rating) {
                    star.textContent = '★';
                    star.classList.add('active');
                } else {
                    star.textContent = '☆';
                    star.classList.remove('active');
                }
            });
        }

        function highlightStars(rating) {
            stars.forEach((star, index) => {
                if (index < rating) {
                    star.textContent = '★';
                } else {
                    star.textContent = '☆';
                }
            });
        }

        function clearStars() {
            stars.forEach(star => {
                star.textContent = '☆';
                star.classList.remove('active');
            });
        }
    }

    // Character Counter for Review Text
    const reviewTextarea = document.getElementById('review_text');
    const charCountElement = document.querySelector('.character-count');

    if (reviewTextarea && charCountElement) {
        function updateCharCount() {
            const currentLength = reviewTextarea.value.length;
            const maxLength = 5000;
            charCountElement.textContent = `${currentLength} / ${maxLength} characters`;

            if (currentLength > maxLength * 0.9) {
                charCountElement.style.color = 'var(--danger-color)';
            } else if (currentLength > maxLength * 0.75) {
                charCountElement.style.color = 'var(--warning-color)';
            } else {
                charCountElement.style.color = 'var(--text-light)';
            }
        }

        reviewTextarea.addEventListener('input', updateCharCount);
        updateCharCount(); // Initial count
    }

    // Form Validation
    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            const rating = ratingInput ? ratingInput.value : null;

            if (!rating || rating < 1 || rating > 5) {
                e.preventDefault();
                alert('Please select a rating (1-5 stars)');
                return false;
            }

            const reviewText = reviewTextarea ? reviewTextarea.value.trim() : '';
            if (reviewText.length < 10) {
                e.preventDefault();
                alert('Review must be at least 10 characters long');
                return false;
            }
        });
    }
});
