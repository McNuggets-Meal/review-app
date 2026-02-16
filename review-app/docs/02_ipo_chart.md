# IPO Chart (Input-Process-Output)
## Movie & Game Review PWA

This document maps the Input-Process-Output flow for all major system functions.

---

## 1. User Registration

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Username | String | 3-50 chars, alphanumeric + underscore | john_doe |
| Email | String | Valid email format | john@example.com |
| Password | String | Minimum 8 characters | SecurePass123! |
| Confirm Password | String | Must match password | SecurePass123! |
| CSRF Token | String | Valid token from session | abc123... |

### PROCESS
1. Receive POST request to /register
2. Validate CSRF token
3. Validate username length (3-50 characters)
4. Validate email format using regex
5. Validate password length (minimum 8 characters)
6. Check password confirmation matches
7. Sanitize inputs (escape special characters)
8. Query database for existing username
9. Query database for existing email
10. If duplicates exist, return error
11. Hash password using bcrypt with 12 rounds
12. Insert new user record into users table
13. Create success flash message
14. Redirect to login page

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| Account created | Username already exists |
| Redirect to login | Email already exists |
| Flash message: "Registration successful" | Invalid email format |
| | Password too short |
| | Passwords don't match |
| | CSRF token invalid |
| | Database error |

### Security Measures
- Password hashed with bcrypt (never stored in plaintext)
- CSRF token validation
- Input sanitization (prevent XSS)
- Parameterized SQL queries (prevent SQL injection)

---

## 2. User Login

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Username | String | Required, not empty | john_doe |
| Password | String | Required, not empty | SecurePass123! |
| CSRF Token | String | Valid token from session | xyz789... |

### PROCESS
1. Receive POST request to /login
2. Validate CSRF token
3. Check username and password are not empty
4. Query database for user by username
5. If user not found, return generic error (no information leakage)
6. Retrieve stored password hash from database
7. Use bcrypt to verify password against hash (constant-time comparison)
8. If password invalid, return generic error
9. If password valid, create session
10. Store user_id and username in session
11. Set session as permanent
12. Redirect to home page with success message

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| User logged in | Invalid credentials (generic message) |
| Session created | CSRF token invalid |
| Redirect to home page | Database error |
| Flash message: "Welcome back, [username]!" | Missing fields |

### Security Measures
- Constant-time password comparison (prevents timing attacks)
- Generic error messages (prevents username enumeration)
- CSRF token validation
- Session cookie flags: HttpOnly, SameSite, Secure (production)
- No password logging or display

---

## 3. User Logout

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Session | Session object | Must be logged in | user_id: 1 |

### PROCESS
1. Receive GET request to /logout
2. Check if user is logged in (session exists)
3. Clear all session data
4. Create success flash message
5. Redirect to home page

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| Session cleared | Already logged out (still redirects) |
| Redirect to home page | |
| Flash message: "You have been logged out" | |

---

## 4. Create Review

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Title | String | 1-200 chars, required | The Matrix |
| Category | String | Must be 'movie' or 'game' | movie |
| Rating | Integer | Must be 1-5 | 5 |
| Review Text | String | 10-5000 chars, required | An excellent sci-fi film... |
| User ID | Integer | From session, required | 1 |
| CSRF Token | String | Valid token from session | def456... |

### PROCESS
1. Check user is logged in (@login_required decorator)
2. If not logged in, redirect to login page
3. Receive POST request to /reviews/create
4. Validate CSRF token
5. Validate title length (1-200 characters)
6. Validate category is 'movie' or 'game'
7. Validate rating is integer between 1 and 5
8. Validate review text length (10-5000 characters)
9. Sanitize all text inputs (escape HTML)
10. Get user_id from session
11. Get current timestamp for review_date
12. Insert review record into reviews table with foreign key to user
13. Create success flash message
14. Redirect to home page or review detail page

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| Review created | Not logged in (redirect to login) |
| Review appears on public page | Invalid category |
| Redirect to reviews page | Rating out of range (1-5) |
| Flash message: "Review posted successfully!" | Title too long |
| | Review text too short/long |
| | CSRF token invalid |
| | Database error |

### Security Measures
- @login_required decorator (authorization)
- CSRF token validation
- Input validation (type and range checking)
- Input sanitization (XSS prevention)
- Parameterized SQL queries

---

## 5. View All Reviews

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Filter: Category | String (optional) | 'movie', 'game', or empty | movie |
| Filter: Rating | Integer (optional) | 1-5 or empty | 5 |

### PROCESS
1. Receive GET request to / or /reviews
2. Check if filters are provided in query parameters
3. Build SQL query with WHERE clause based on filters
4. Join reviews table with users table to get usernames
5. Order reviews by review_date DESC (most recent first)
6. Execute query with parameterized values
7. Fetch all matching reviews
8. Format review_date for display
9. Truncate review_text for excerpt (first 150 characters)
10. Pass reviews to template
11. Render HTML with Jinja2 (auto-escaping enabled)

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| List of reviews displayed | Database error |
| Each review shows: | No reviews found (show empty state) |
| - Title | |
| - Category badge | |
| - Star rating visualization | |
| - Review excerpt | |
| - Author username | |
| - Review date | |
| - Link to full review | |

### Security Measures
- Jinja2 auto-escaping (XSS prevention)
- Parameterized SQL queries
- Public access (no sensitive data exposed)

---

## 6. View Single Review

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Review ID | Integer | Must exist in database | 5 |
| User ID (session) | Integer (optional) | For showing edit/delete buttons | 1 |

### PROCESS
1. Receive GET request to /reviews/<review_id>
2. Validate review_id is integer
3. Query database for review by ID
4. Join with users table to get author username
5. If review not found, return 404 error
6. Check if logged-in user is the review author
7. Pass review data to template
8. Pass ownership flag to template
9. Render HTML with full review details

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| Full review displayed | Review not found (404) |
| Shows: | Invalid review ID |
| - Title | Database error |
| - Category | |
| - Star rating | |
| - Full review text | |
| - Author username | |
| - Review date | |
| - Updated date (if edited) | |
| - Edit/Delete buttons (if owner) | |

### Security Measures
- Jinja2 auto-escaping
- Parameterized SQL queries
- Conditional display of edit/delete based on ownership

---

## 7. Edit Review

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Review ID | Integer | Must exist and be owned by user | 5 |
| Title | String | 1-200 chars, required | The Matrix (Updated) |
| Category | String | Must be 'movie' or 'game' | movie |
| Rating | Integer | Must be 1-5 | 4 |
| Review Text | String | 10-5000 chars, required | Updated review text... |
| User ID | Integer | From session | 1 |
| CSRF Token | String | Valid token | ghi789... |

### PROCESS
1. Check user is logged in (@login_required decorator)
2. Receive GET request to /reviews/<review_id>/edit (show form)
3. Query database for review by ID
4. Check review.user_id matches session user_id
5. If not owner, return 403 Forbidden
6. Pre-populate form with existing review data
7. Render edit form
8. (On form submission) Receive POST request
9. Validate CSRF token
10. Validate all input fields (same as create review)
11. Verify ownership again
12. Sanitize inputs
13. Update review record in database
14. Set updated_at timestamp to current time
15. Create success flash message
16. Redirect to updated review detail page

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| Review updated | Not logged in (redirect) |
| Updated timestamp changed | Not review owner (403) |
| Redirect to review detail | Review not found (404) |
| Flash message: "Review updated successfully!" | Validation errors |
| | CSRF token invalid |

### Security Measures
- @login_required decorator
- Ownership verification (prevents unauthorized edits)
- CSRF token validation
- Input validation and sanitization
- Parameterized SQL queries

---

## 8. Delete Review

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Review ID | Integer | Must exist and be owned by user | 5 |
| User ID | Integer | From session | 1 |
| CSRF Token | String | Valid token | jkl012... |

### PROCESS
1. Check user is logged in (@login_required decorator)
2. Receive POST request to /reviews/<review_id>/delete
3. Validate CSRF token
4. Query database for review by ID
5. If review not found, return 404 error
6. Check review.user_id matches session user_id
7. If not owner, return 403 Forbidden
8. Delete review record from database
9. Create success flash message
10. Redirect to user's reviews page

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| Review deleted | Not logged in (redirect) |
| Record removed from database | Not review owner (403) |
| Redirect to "My Reviews" | Review not found (404) |
| Flash message: "Review deleted successfully!" | CSRF token invalid |
| | Database error |

### Security Measures
- @login_required decorator
- Ownership verification (prevents unauthorized deletion)
- CSRF token validation
- Parameterized SQL queries
- ON DELETE CASCADE (if user deleted, reviews auto-deleted)

---

## 9. View My Reviews

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| User ID | Integer | From session, required | 1 |

### PROCESS
1. Check user is logged in (@login_required decorator)
2. If not logged in, redirect to login page
3. Receive GET request to /reviews/my
4. Get user_id from session
5. Query database for all reviews where user_id matches
6. Order by review_date DESC
7. Pass reviews to template
8. Render HTML with user's reviews and edit/delete options

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| List of user's own reviews | Not logged in (redirect) |
| Each review has edit/delete buttons | Database error |
| Shows count of total reviews | No reviews (show empty state) |
| Link to create new review | |

### Security Measures
- @login_required decorator
- Only shows reviews belonging to logged-in user
- CSRF tokens in delete forms

---

## 10. Filter Reviews

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Category | String (optional) | 'movie', 'game', or 'all' | movie |
| Rating | Integer (optional) | 1-5 or 'all' | 5 |

### PROCESS
1. Receive GET request to / or /reviews with query parameters
2. Parse query parameters (category, rating)
3. Validate category is valid option
4. Validate rating is 1-5 if provided
5. Build SQL WHERE clause dynamically
6. Execute query with parameterized values
7. Fetch matching reviews
8. Pass to template
9. Render filtered results
10. Preserve filter selections in UI

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| Filtered list of reviews | Invalid filter value (ignore) |
| Filter UI shows active selections | Database error |
| Count of results shown | No results (show empty state) |

### Security Measures
- Input validation
- Parameterized SQL queries
- Jinja2 auto-escaping

---

## 11. Service Worker - Cache Resources (PWA)

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| Resource URLs | Array of strings | Valid URLs | ['/static/css/main.css', ...] |

### PROCESS
1. Service worker install event fires
2. Open cache storage with version name
3. Fetch all specified resources
4. Store responses in cache
5. Complete installation

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| Resources cached | Network error (retry) |
| Service worker active | Cache storage full |

---

## 12. Service Worker - Serve Cached Content (PWA)

### INPUT
| Field | Type | Validation | Example |
|-------|------|------------|---------|
| HTTP Request | Request object | Valid request | GET /static/css/main.css |

### PROCESS
1. Service worker fetch event fires
2. Check if request matches cached resource
3. If match found, serve from cache
4. If no match, fetch from network
5. Optionally cache network response
6. Return response

### OUTPUT
| Success Case | Error Cases |
|--------------|-------------|
| Resource served (cache or network) | Network offline + not cached |
| Fast response from cache | |

---

## Summary Table

| Function | Primary Input | Key Process | Primary Output |
|----------|---------------|-------------|----------------|
| Register | Username, email, password | Validate, hash, insert DB | Account created |
| Login | Username, password | Verify hash, create session | Session established |
| Logout | Session | Clear session | Redirect to home |
| Create Review | Title, rating, text, category | Validate, sanitize, insert DB | Review published |
| View All | Optional filters | Query DB, format | List of reviews |
| View Single | Review ID | Query DB, check ownership | Full review |
| Edit Review | Review ID, updated fields | Verify ownership, update DB | Review updated |
| Delete Review | Review ID | Verify ownership, delete DB | Review removed |
| My Reviews | User ID (session) | Query user's reviews | User's review list |
| Filter | Category, rating | Build query, execute | Filtered results |

---

## Data Flow Diagram

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────────────────┐
│   Flask Application     │
│                         │
│  ┌──────────────────┐   │
│  │  Route Handler   │   │
│  └────────┬─────────┘   │
│           │             │
│           ▼             │
│  ┌──────────────────┐   │
│  │   Middleware     │   │
│  │  (Auth, CSRF)    │   │
│  └────────┬─────────┘   │
│           │             │
│           ▼             │
│  ┌──────────────────┐   │
│  │   Validators     │   │
│  └────────┬─────────┘   │
│           │             │
│           ▼             │
│  ┌──────────────────┐   │
│  │     Models       │   │
│  │  (User, Review)  │   │
│  └────────┬─────────┘   │
│           │             │
└───────────┼─────────────┘
            │ SQL Query
            ▼
   ┌────────────────┐
   │ SQLite Database│
   │                │
   │ ┌───────────┐  │
   │ │  users    │  │
   │ └───────────┘  │
   │ ┌───────────┐  │
   │ │  reviews  │  │
   │ └───────────┘  │
   └────────────────┘
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-29 | Development Team | Initial IPO chart |
