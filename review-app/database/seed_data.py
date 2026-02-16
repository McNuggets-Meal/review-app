"""
Database Seeding Script
Populates the database with sample users, movies/games, and reviews
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

# Import bcrypt for password hashing
try:
    import bcrypt
except ImportError:
    print("Error: bcrypt not installed. Run: pip install bcrypt")
    sys.exit(1)

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=config.BCRYPT_LOG_ROUNDS)).decode('utf-8')

def seed_database():
    """Populate database with sample data"""

    if not os.path.exists(config.DATABASE_PATH):
        print(f"Error: Database not found at {config.DATABASE_PATH}")
        print("Please run init_db.py first")
        return

    print(f"Seeding database at: {config.DATABASE_PATH}")
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    try:
        # === CREATE USERS ===
        print("\n=== Creating Users ===")

        users = [
            ('john_doe', 'john@example.com', 'SecurePass123!'),
            ('jane_smith', 'jane@example.com', 'JaneSecure456!'),
            ('alex_wong', 'alex@example.com', 'AlexPass789!')
        ]

        for username, email, password in users:
            password_hash = hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            print(f"[OK] Created user: {username} ({email})")

        conn.commit()
        print(f"\nTotal users created: {len(users)}")

        # === CREATE REVIEWS ===
        print("\n=== Creating Reviews ===")

        # Define reviews with: (user_id, title, review_text, rating, category, days_ago)
        reviews = [
            # User 1 (john_doe) reviews
            (1, 'The Matrix', 'A groundbreaking sci-fi film that explores the nature of reality and consciousness. The action sequences are innovative and the philosophical themes are thought-provoking. Keanu Reeves delivers an iconic performance as Neo. A must-watch for any sci-fi fan.', 5, 'movie', 10),
            (1, 'Inception', 'Mind-bending thriller with incredible visuals and a complex plot. Christopher Nolan at his finest. The layered dream sequences are brilliantly executed, and the ending leaves you questioning everything. Hans Zimmer\'s score is phenomenal.', 5, 'movie', 9),
            (1, 'Interstellar', 'Epic science fiction masterpiece about love, time, and survival. Stunning visuals and emotional depth. The portrayal of black holes and relativity is both scientifically grounded and visually spectacular. Matthew McConaughey gives one of his best performances.', 5, 'movie', 8),
            (1, 'Cyberpunk 2077', 'After the updates, this game has become truly amazing. The world of Night City is incredibly detailed and immersive. The story is engaging, characters are memorable, and the gameplay is satisfying. Still has some bugs but the overall experience is fantastic.', 4, 'game', 5),

            # User 2 (jane_smith) reviews
            (2, 'Hollow Knight', 'An absolute masterpiece of game design. The hand-drawn art style is breathtaking, and the challenging gameplay keeps you engaged for hours. The exploration is rewarding and the boss fights are memorable. One of the best Metroidvania games ever made.', 5, 'game', 7),
            (2, 'The Witcher 3', 'Best RPG I\'ve ever played. Rich storytelling, complex characters, and a massive world to explore. Every quest feels meaningful, and the moral choices genuinely matter. Geralt is a fantastic protagonist, and the DLCs are even better than the base game.', 5, 'game', 6),
            (2, 'Dune', 'Visually stunning adaptation of Frank Herbert\'s epic novel. Denis Villeneuve\'s direction is masterful. The cinematography, score, and performances all come together perfectly. Can\'t wait for Part Two. Timothée Chalamet and Zendaya are excellent.', 5, 'movie', 4),
            (2, 'The Matrix', 'Revolutionary film that changed action cinema forever. The bullet-time effects were groundbreaking for 1999. The story about reality and choice is still relevant today. A perfect blend of philosophy and action.', 5, 'movie', 12),

            # User 3 (alex_wong) reviews
            (3, 'Elden Ring', 'An absolute masterpiece that combines the best elements of Dark Souls with an expansive open world. The difficulty is challenging but fair, and every victory feels earned. The lore is deep and mysterious, typical of FromSoftware. George R.R. Martin\'s contributions to the worldbuilding are evident.', 5, 'game', 3),
            (3, 'Hollow Knight', 'Incredibly atmospheric Metroidvania with tight controls and beautiful art. The difficulty curve is perfect, and the sense of exploration is unmatched. Team Cherry created something truly special. Every area has its own distinct feel and challenges.', 5, 'game', 11),
            (3, 'Inception', 'Christopher Nolan\'s masterpiece. The concept of dreams within dreams is executed flawlessly. Leonardo DiCaprio leads an excellent cast. The practical effects still hold up perfectly. That ending though - still debating it years later!', 5, 'movie', 13),
            (3, 'The Witcher 3', 'Incredible open-world RPG with amazing storytelling. CD Projekt Red set the bar high. Geralt\'s journey is emotional and engaging. The Bloody Baron questline alone is worth the price of admission. Hearts of Stone and Blood and Wine DLCs are essential.', 5, 'game', 14),

            # Additional reviews for variety
            (1, 'Dune', 'Denis Villeneuve proves once again he\'s a visionary director. The scale and scope of this film are breathtaking. The desert planet Arrakis feels real and dangerous. Looking forward to seeing how they conclude the story.', 4, 'movie', 2),
            (2, 'Elden Ring', 'FromSoftware\'s magnum opus. The open-world format breathes new life into the Souls formula. So much content and replayability. The boss designs are some of the best in gaming. Prepare to die... a lot.', 5, 'game', 1),
            (3, 'Cyberpunk 2077', 'The game has come a long way since launch. Night City is one of the most detailed game worlds ever created. The story of V and Johnny Silverhand is compelling. Keanu Reeves\' performance as Johnny is excellent. Worth playing now after all the patches.', 4, 'game', 2),
        ]

        for user_id, title, review_text, rating, category, days_ago in reviews:
            # Calculate review_date (recent reviews)
            review_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(
                "INSERT INTO reviews (user_id, title, review_text, rating, review_date, category) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, title, review_text, rating, review_date, category)
            )
            print(f"[OK] Created review: {title} ({category}) - {rating}* by user {user_id}")

        conn.commit()
        print(f"\nTotal reviews created: {len(reviews)}")

        # === SUMMARY ===
        print("\n" + "=" * 60)
        print("DATABASE SEEDING COMPLETE!")
        print("=" * 60)

        # Count by category
        cursor.execute("SELECT category, COUNT(*) FROM reviews GROUP BY category")
        categories = cursor.fetchall()
        print("\nReviews by category:")
        for category, count in categories:
            print(f"  {category.capitalize()}: {count}")

        # Count unique titles
        cursor.execute("SELECT COUNT(DISTINCT title) FROM reviews")
        unique_titles = cursor.fetchone()[0]
        print(f"\nUnique movies/games: {unique_titles}")

        # Show sample login credentials
        print("\n" + "=" * 60)
        print("SAMPLE LOGIN CREDENTIALS:")
        print("=" * 60)
        for username, email, password in users:
            print(f"Username: {username}")
            print(f"Password: {password}")
            print(f"Email: {email}")
            print("-" * 60)

        print("\nYou can now run the application with: python app.py")

    except sqlite3.Error as e:
        print(f"\n[ERROR] Error seeding database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    seed_database()
