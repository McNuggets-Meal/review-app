-- Database Schema for Movie & Game Review PWA
-- SQLite3 Database

-- Enable foreign key constraints (must be done per connection)
PRAGMA foreign_keys = ON;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL CHECK(length(username) >= 3 AND length(username) <= 50),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL CHECK(length(password_hash) = 60),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL CHECK(length(title) >= 1 AND length(title) <= 200),
    review_text TEXT NOT NULL CHECK(length(review_text) >= 10 AND length(review_text) <= 5000),
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    category TEXT NOT NULL CHECK(category IN ('movie', 'game')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_category ON reviews(category);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date DESC);
