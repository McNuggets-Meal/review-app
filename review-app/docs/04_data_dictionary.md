# Data Dictionary
## Movie & Game Review PWA Database

Complete specification of all database tables, fields, datatypes, constraints, and relationships.

---

## Database: reviews_app.db (SQLite3)

### Foreign Key Constraints: ENABLED
```sql
PRAGMA foreign_keys = ON;
```

---

## Table 1: users

**Purpose:** Stores user account information including authentication credentials.

| Field Name | Data Type | Size/Precision | Constraints | Default Value | Description | Example |
|------------|-----------|----------------|-------------|---------------|-------------|---------|
| id | INTEGER | - | PRIMARY KEY, AUTOINCREMENT, NOT NULL | AUTO | Unique identifier for each user | 1 |
| username | TEXT | 3-50 chars | UNIQUE, NOT NULL | - | User's display name for login and attribution | john_doe |
| email | TEXT | Valid email | UNIQUE, NOT NULL | - | User's email address for account identification | john@example.com |
| password_hash | TEXT | 60 chars | NOT NULL | - | Bcrypt hash of user's password (never store plaintext) | $2b$12$... |
| created_at | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | Date and time when account was created | 2026-01-29 10:30:45 |

### Indexes
- `PRIMARY KEY` on `id` (automatic)
- `UNIQUE INDEX` on `username` (automatic from UNIQUE constraint)
- `UNIQUE INDEX` on `email` (automatic from UNIQUE constraint)

### Business Rules
1. Username must be 3-50 characters, alphanumeric plus underscore
2. Email must match valid email format regex
3. Password must be minimum 8 characters before hashing
4. Password hash is generated using bcrypt with 12 rounds
5. Usernames and emails are case-sensitive for SQLite
6. Deletion of user cascades to delete all their reviews

### Sample Data
```sql
id: 1
username: john_doe
email: john@example.com
password_hash: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztK4F7nKcSDO
created_at: 2026-01-20 14:23:11

id: 2
username: jane_smith
email: jane@example.com
password_hash: $2b$12$EHqF9aKw1hZ0qNxL8R8r4.YqQvX9rZ1K3nD5mS7tP8wR2qN4xL6vO
created_at: 2026-01-21 09:15:33

id: 3
username: alex_wong
email: alex@example.com
password_hash: $2b$12$NpR7sT2vK8qL5wM3nQ9fR.XzS1pT4uY6vZ8wA2bC5dE7fG9hJ1kM3
created_at: 2026-01-22 16:47:22
```

---

## Table 2: reviews

**Purpose:** Stores user-submitted reviews for movies and games.

| Field Name | Data Type | Size/Precision | Constraints | Default Value | Description | Example |
|------------|-----------|----------------|-------------|---------------|-------------|---------|
| id | INTEGER | - | PRIMARY KEY, AUTOINCREMENT, NOT NULL | AUTO | Unique identifier for each review | 1 |
| user_id | INTEGER | - | FOREIGN KEY (users.id), NOT NULL | - | ID of user who created this review | 1 |
| title | TEXT | 1-200 chars | NOT NULL | - | Name of the movie or game being reviewed | The Matrix |
| review_text | TEXT | 10-5000 chars | NOT NULL | - | Full text of the review | An excellent sci-fi film that... |
| rating | INTEGER | 1-5 | NOT NULL, CHECK(rating >= 1 AND rating <= 5) | - | Star rating from 1 (worst) to 5 (best) | 5 |
| review_date | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | Date and time when review was created | 2026-01-29 11:20:30 |
| updated_at | TIMESTAMP | - | NULL | NULL | Date and time when review was last edited (NULL if never edited) | 2026-01-30 14:15:00 |
| category | TEXT | - | NOT NULL, CHECK(category IN ('movie', 'game')) | - | Type of media being reviewed | movie |

### Indexes
- `PRIMARY KEY` on `id` (automatic)
- `INDEX idx_reviews_user_id` on `user_id` (for efficient JOIN and filtering)
- `INDEX idx_reviews_category` on `category` (for filtering)
- `INDEX idx_reviews_rating` on `rating` (for filtering)

### Foreign Keys
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE
  - If a user is deleted, all their reviews are automatically deleted

### Check Constraints
1. `rating >= 1 AND rating <= 5` - Ensures rating is between 1 and 5 inclusive
2. `category IN ('movie', 'game')` - Only allows these two category values

### Business Rules
1. Title must be 1-200 characters
2. Review text must be 10-5000 characters
3. Rating must be whole number from 1 to 5 (no decimals)
4. Category must be exactly 'movie' or 'game' (lowercase)
5. Review_date is automatically set on creation
6. Updated_at is NULL until first edit, then set to current timestamp
7. Users can only edit/delete their own reviews (enforced in application layer)
8. All text inputs are sanitized to prevent XSS

### Sample Data
```sql
id: 1
user_id: 1
title: The Matrix
review_text: A groundbreaking sci-fi film that explores the nature of reality and consciousness. The action sequences are innovative and the philosophical themes are thought-provoking. A must-watch for any sci-fi fan.
rating: 5
review_date: 2026-01-22 15:30:00
updated_at: NULL
category: movie

id: 2
user_id: 2
title: Hollow Knight
review_text: An absolute masterpiece of game design. The hand-drawn art style is breathtaking, and the challenging gameplay keeps you engaged for hours. The exploration is rewarding and the boss fights are memorable.
rating: 5
review_date: 2026-01-25 18:45:22
updated_at: NULL
category: game

id: 3
user_id: 1
title: Inception
review_text: Mind-bending thriller with incredible visuals and a complex plot. Christopher Nolan at his finest. The layered dream sequences are brilliantly executed.
rating: 4
review_date: 2026-01-20 20:10:15
updated_at: 2026-01-25 14:30:00
category: movie

id: 4
user_id: 3
title: Elden Ring
review_text: An absolute masterpiece that combines the best elements of Dark Souls with an expansive open world. The difficulty is challenging but fair, and every victory feels earned. The lore is deep and mysterious.
rating: 5
review_date: 2026-01-28 12:00:00
updated_at: NULL
category: game
```

---

## Entity Relationship Diagram (ERD)

```
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ PK  id              │
│     username (UQ)   │
│     email (UQ)      │
│     password_hash   │
│     created_at      │
└─────────┬───────────┘
          │
          │ 1
          │
          │
          │ *
┌─────────▼───────────┐
│      reviews        │
├─────────────────────┤
│ PK  id              │
│ FK  user_id         │◄──── ON DELETE CASCADE
│     title           │
│     review_text     │
│     rating          │
│     review_date     │
│     updated_at      │
│     category        │
└─────────────────────┘

Relationship: One-to-Many
- One user can have many reviews (0 to N)
- One review belongs to exactly one user
- Cascade delete: Deleting user deletes all their reviews
```

---

## Relationship Details

### users → reviews (One-to-Many)

**Cardinality:** 1:M (One user to Many reviews)

**Participation:**
- User: Partial (a user may have zero reviews)
- Review: Total (every review must have a user)

**Foreign Key:** reviews.user_id → users.id

**Delete Rule:** CASCADE (deleting a user deletes all their reviews)

**Update Rule:** CASCADE (if user.id changes, reviews.user_id updates automatically)

**Business Logic:**
- A user can create unlimited reviews
- A user can review the same movie/game multiple times (not restricted at DB level)
- Reviews must be attributed to a valid user account
- Anonymous reviews are not allowed

---

## Data Validation Rules

### Application-Level Validation (Before Database)

#### Username Validation
- Minimum length: 3 characters
- Maximum length: 50 characters
- Allowed characters: a-z, A-Z, 0-9, underscore (_)
- Cannot contain spaces
- Case-sensitive
- Must be unique (checked against database)

**Regex:** `^[a-zA-Z0-9_]{3,50}$`

#### Email Validation
- Must match standard email format
- Must contain @ symbol
- Must have domain extension
- Must be unique (checked against database)

**Regex:** `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

#### Password Validation (Pre-Hash)
- Minimum length: 8 characters
- Maximum length: 128 characters (before hashing)
- Should contain mix of uppercase, lowercase, numbers (recommended but not enforced)
- Never stored in plaintext
- Always hashed with bcrypt (12 rounds) before storage

#### Review Title Validation
- Minimum length: 1 character
- Maximum length: 200 characters
- Cannot be only whitespace
- HTML entities escaped for XSS protection

#### Review Text Validation
- Minimum length: 10 characters
- Maximum length: 5000 characters
- Cannot be only whitespace
- HTML entities escaped for XSS protection

#### Rating Validation
- Must be integer
- Minimum value: 1
- Maximum value: 5
- No decimal values allowed

#### Category Validation
- Must be exactly 'movie' or 'game'
- Case-sensitive (lowercase only)
- No other values accepted

---

## Security Considerations

### Password Storage
- **Never store plaintext passwords**
- Use bcrypt with 12 rounds (configurable)
- Hash format: `$2b$12$[22 char salt][31 char hash]`
- Total length: 60 characters

### SQL Injection Prevention
- All queries use parameterized statements
- Use `?` placeholders in SQLite
- Never concatenate user input into SQL strings

### XSS Prevention
- All user inputs sanitized before storage
- Jinja2 auto-escaping enabled in templates
- HTML entities escaped: `<script>` becomes `&lt;script&gt;`

### CSRF Protection
- Tokens generated per session
- Validated on all POST/PUT/DELETE operations
- Tokens stored in forms as hidden fields

---

## Database Size Estimates

### Storage Calculations (Approximate)

**Per User Record:**
- id: 4 bytes (INTEGER)
- username: 25 bytes average (TEXT)
- email: 30 bytes average (TEXT)
- password_hash: 60 bytes (TEXT)
- created_at: 8 bytes (TIMESTAMP)
- **Total per user: ~127 bytes**

**Per Review Record:**
- id: 4 bytes (INTEGER)
- user_id: 4 bytes (INTEGER)
- title: 30 bytes average (TEXT)
- review_text: 500 bytes average (TEXT)
- rating: 4 bytes (INTEGER)
- review_date: 8 bytes (TIMESTAMP)
- updated_at: 8 bytes (TIMESTAMP, nullable)
- category: 6 bytes average (TEXT)
- **Total per review: ~564 bytes**

**Estimated Database Size:**
- 1,000 users: 127 KB
- 10,000 reviews: 5.64 MB
- Indexes: ~10-20% overhead
- **Total for demo: < 10 MB**

---

## Backup and Maintenance

### Backup Strategy
- SQLite database is single file: `reviews_app.db`
- Copy file to backup location regularly
- Consider using SQLite `.backup` command
- Store backups off-site or in version control (with .gitignore for main DB)

### Maintenance Tasks
- **Vacuum:** Reclaim unused space periodically
  ```sql
  VACUUM;
  ```
- **Analyze:** Update query optimizer statistics
  ```sql
  ANALYZE;
  ```
- **Integrity Check:** Verify database integrity
  ```sql
  PRAGMA integrity_check;
  ```

---

## Migration Considerations

### Future Schema Changes
If schema needs to change:
1. Use SQLite ALTER TABLE (limited capabilities)
2. Or create new table, copy data, drop old, rename new
3. Consider Flask-Migrate or Alembic for version control
4. Always backup before migration

### Possible Future Fields
- users table:
  - `profile_picture` (TEXT - URL or base64)
  - `bio` (TEXT - user description)
  - `is_admin` (BOOLEAN - admin flag)
- reviews table:
  - `likes_count` (INTEGER - number of likes)
  - `is_featured` (BOOLEAN - featured review flag)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-29 | Development Team | Initial data dictionary |
