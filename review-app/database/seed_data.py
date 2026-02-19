"""
Database Seeding Script
Populates the database with sample users and Persona series reviews
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
            ('alex_tehvand',    'alex@example.com',   'SecurePass123!'),
            ('reuben_sandwich', 'reuben@example.com', 'JaneSecure456!'),
            ('wong_wongster',   'wong@example.com',   'AlexPass789!'),
            ('anonymous',       'anon@example.com',   'AnonPass000!'),
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

        # user_id key:
        #   1 = alex_tehvand       — reviews: Revelations: Persona, Persona 3 FES, Persona 5 Royal
        #   2 = reuben_sandwich    — reviews: Persona 2: Innocent Sin, Persona 4 Golden, Persona 3 ReLoad
        #   3 = wong_wongster      — reviews: Persona 2: Eternal Punishment, Persona Q, Persona 5 Royal
        #   4 = anonymous          — one review for every game

        # Format: (user_id, title, review_text, rating, category, days_ago)
        reviews = [

            # ── alex_tehvand (user 1) ── 3 reviews
            (1, 'Revelations: Persona',
             'A rough but fascinating start to the Persona series. The dungeon crawling is repetitive by modern standards but the demon negotiation system and dark atmosphere kept me hooked. You can clearly see the DNA of everything that came after. Essential for any serious Persona fan wanting to understand the origins of the series.',
             4, 'game', 20),

            (1, 'Persona 3 FES',
             'Persona 3 FES is an emotionally devastating experience that I will never forget. The themes of death and mortality are handled with such maturity and care. The cast of SEES feel like real people and watching their journeys unfold over the school year is deeply moving. Tartarus gets repetitive but the story more than makes up for it. The Answer epilogue adds a bitter but satisfying conclusion.',
             5, 'game', 12),

            (1, 'Persona 5 Royal',
             'An absolute masterpiece from start to finish. Persona 5 Royal refines everything the base game did and adds a genuinely touching new semester that recontextualises the whole story. The art style is the most stylish thing in gaming, the soundtrack is incredible, and every Phantom Thief feels fully realised. Easily one of the greatest JRPGs ever made.',
             5, 'game', 4),

            # ── reuben_sandwich (user 2) ── 3 reviews
            (2, 'Persona 2: Innocent Sin',
             'Innocent Sin is a wildly ambitious game with one of the darkest and most mature stories in the entire series. The rumour system is a genuinely clever mechanic and the villain is terrifying. The combat is a little dated but the character writing is outstanding, especially Tatsuya and his friends. The ending hit me harder than I expected. A hidden gem that deserves far more attention.',
             4, 'game', 18),

            (2, 'Persona 4 Golden',
             'Persona 4 Golden is pure comfort food JRPG perfection. The murder mystery plot is compelling, Inaba feels like a real town you want to live in, and the social links are some of the best written in the series. Golden adds Marie and extra content that genuinely enriches the experience. The gameplay loop of dungeon crawling and managing your social life is endlessly satisfying. A timeless classic.',
             5, 'game', 9),

            (2, 'Persona 3 ReLoad',
             'ReLoad is the definitive way to experience Persona 3. The visual overhaul is stunning, the new voice cast is excellent, and the quality of life improvements make the dungeons far less of a slog. Seeing this story with modern polish brought tears to my eyes all over again. My only complaint is the absence of The Answer but as a remake of the base game it is flawless.',
             5, 'game', 2),

            # ── wong_wongster (user 3) ── 3 reviews
            (3, 'Persona 2: Eternal Punishment',
             'Eternal Punishment tells the same story as Innocent Sin from the other side and does it brilliantly. Maya Amano is a fantastic protagonist and the more grounded cast of adults gives the game a completely different tone to the rest of the series. The gameplay is the same as IS but the narrative payoff for playing both games is immense. One of the most underrated games in the franchise.',
             5, 'game', 16),

            (3, 'Persona Q: Shadow of the Labyrinth',
             'A fun crossover between Persona 3 and 4 that works better than it has any right to. The Etrian Odyssey dungeon crawling formula suits the Persona characters surprisingly well and the interactions between the two casts are entertaining throughout. It is clearly fan service but it is well crafted fan service. Not the best entry point for newcomers but fans of both games will enjoy it.',
             3, 'game', 7),

            (3, 'Persona 5 Royal',
             'I came into Persona 5 Royal with sky high expectations and it somehow exceeded them. The heist framing for the dungeons is genius, the Palaces are all memorable and creative, and Joker might be the coolest silent protagonist in JRPG history. The third semester added in Royal wraps everything up in a way that left me staring at the credits in silence. An unforgettable experience.',
             5, 'game', 3),

            # ── anonymous (user 4) ── one review per game
            (4, 'Revelations: Persona',
             'Dated but interesting. The first Persona game shows its age in almost every system but the dark tone and experimental ideas make it worth experiencing if you are curious about where the series began. Manage your expectations and you might find something genuinely compelling underneath the rough exterior.',
             3, 'game', 25),

            (4, 'Persona 2: Innocent Sin',
             'The story in Innocent Sin is unlike anything else in the series. It goes to genuinely dark places and the cast dynamic is excellent. The combat system has not aged particularly well but the writing carries it. If you can look past the dated mechanics there is a deeply emotional game here that stands up alongside the modern entries.',
             4, 'game', 22),

            (4, 'Persona 2: Eternal Punishment',
             'A worthy companion to Innocent Sin. Eternal Punishment reframes events in a way that adds real depth to the duology. Maya is a great lead and the tone feels distinct from everything else Atlus has made. Playing both Persona 2 games together is one of the best storytelling experiences the series has to offer.',
             4, 'game', 21),

            (4, 'Persona 3 FES',
             'Persona 3 FES changed what I thought a JRPG could be. The memento mori theme runs through every part of the game and it never feels heavy handed. The social simulation elements blend seamlessly with the dungeon crawling and the final stretch of the game is one of the most powerful sequences in gaming. FES is the version to play.',
             5, 'game', 15),

            (4, 'Persona 4 Golden',
             'Persona 4 Golden is one of the most purely enjoyable games I have ever played. It is warm, funny, and surprisingly emotional when it wants to be. The mystery plot keeps you engaged for the entire runtime and the Golden additions improve an already great game. If you only ever play one Persona game make it this one.',
             5, 'game', 11),

            (4, 'Persona Q: Shadow of the Labyrinth',
             'A decent side game that fans of Persona 3 and 4 will get the most out of. The chibi art style is charming and the dungeon design is solid if unspectacular. The story is lightweight compared to the mainline games but it is a fun excuse to see the two casts interact. Worth playing during a gap between the bigger entries.',
             3, 'game', 8),

            (4, 'Persona 5 Royal',
             'Persona 5 Royal deserves every piece of praise it receives. The game oozes style from the menu screens to the battle transitions to the incredible soundtrack. The story about rebelling against corrupt authority figures resonates strongly and the characters are all loveable. Royal takes an already brilliant game and makes it essential. A genuine landmark for the genre.',
             5, 'game', 5),

            (4, 'Persona 3 ReLoad',
             'ReLoad is proof that great games only get better with love and care. The Persona 3 story is one of the best in the series and ReLoad presents it with a level of visual and audio polish that feels truly modern. The new social link content adds welcome texture to characters who were previously underserved. An outstanding remake that respects the original while making it accessible to a new generation.',
             5, 'game', 1),
        ]

        for user_id, title, review_text, rating, category, days_ago in reviews:
            review_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO reviews (user_id, title, review_text, rating, review_date, category) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, title, review_text, rating, review_date, category)
            )
            print(f"[OK] Created review: {title} - {rating}* by user {user_id}")

        conn.commit()
        print(f"\nTotal reviews created: {len(reviews)}")

        # === SUMMARY ===
        print("\n" + "=" * 60)
        print("DATABASE SEEDING COMPLETE!")
        print("=" * 60)

        cursor.execute("SELECT COUNT(DISTINCT title) FROM reviews")
        unique_titles = cursor.fetchone()[0]
        print(f"\nUnique games:   {unique_titles}")
        print(f"Total reviews:  {len(reviews)}")

        print("\n" + "=" * 60)
        print("SAMPLE LOGIN CREDENTIALS:")
        print("=" * 60)
        for username, email, password in users:
            print(f"Username: {username}")
            print(f"Password: {password}")
            print(f"Email:    {email}")
            print("-" * 60)

        print("\nYou can now run the application with: python app.py")

    except sqlite3.Error as e:
        print(f"\n[ERROR] Error seeding database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    seed_database()
