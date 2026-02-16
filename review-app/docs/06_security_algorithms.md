# Security Algorithms
## Movie & Game Review PWA

This document contains detailed pseudocode and flowcharts for all security-critical operations in the application.

---

## 1. User Registration Algorithm

### Purpose
Securely create a new user account with hashed password and prevent duplicate accounts.

### Pseudocode

```
ALGORITHM RegisterUser(username, email, password, confirm_password, csrf_token)

INPUT:
    username: string (from form)
    email: string (from form)
    password: string (from form)
    confirm_password: string (from form)
    csrf_token: string (from hidden form field)

OUTPUT:
    success: redirect to login page with flash message
    OR
    error: re-display form with error messages

BEGIN

    // Step 1: CSRF Protection
    IF NOT validate_csrf_token(csrf_token, session['csrf_token']) THEN
        RETURN error("Invalid CSRF token. Please try again.")
    END IF

    // Step 2: Input Validation
    IF length(username) < 3 OR length(username) > 50 THEN
        RETURN error("Username must be between 3 and 50 characters.")
    END IF

    IF NOT matches_pattern(username, "^[a-zA-Z0-9_]+$") THEN
        RETURN error("Username can only contain letters, numbers, and underscores.")
    END IF

    IF NOT is_valid_email(email) THEN
        RETURN error("Please enter a valid email address.")
    END IF

    IF length(password) < 8 THEN
        RETURN error("Password must be at least 8 characters long.")
    END IF

    IF password != confirm_password THEN
        RETURN error("Passwords do not match.")
    END IF

    // Step 3: Sanitize Inputs (XSS Prevention)
    username = sanitize_html(username)
    email = sanitize_html(email)
    // Note: password is NOT sanitized (would weaken it)

    // Step 4: Check for Duplicate Username
    existing_user = database.query(
        "SELECT id FROM users WHERE username = ?",
        [username]
    )

    IF existing_user IS NOT NULL THEN
        RETURN error("Username already taken. Please choose another.")
    END IF

    // Step 5: Check for Duplicate Email
    existing_email = database.query(
        "SELECT id FROM users WHERE email = ?",
        [email]
    )

    IF existing_email IS NOT NULL THEN
        RETURN error("An account with this email already exists.")
    END IF

    // Step 6: Hash Password (bcrypt with 12 rounds)
    password_hash = bcrypt.generate_password_hash(
        password,
        rounds=12
    )
    // Result format: $2b$12$[22 char salt][31 char hash]
    // Total length: 60 characters

    // Step 7: Insert New User
    TRY
        user_id = database.execute(
            "INSERT INTO users (username, email, password_hash, created_at)
             VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            [username, email, password_hash]
        )

        // Step 8: Success Response
        flash_message("Registration successful! Please log in.")
        RETURN redirect("/login")

    CATCH DatabaseError AS e
        log_error("Registration failed for username: " + username, e)
        RETURN error("Registration failed. Please try again.")
    END TRY

END ALGORITHM
```

### Flowchart

```
┌─────────────────────┐
│  Start: User submits│
│  registration form  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Validate CSRF token│
└──────────┬──────────┘
           │
      ┌────▼────┐
      │ Valid?  │
      └────┬────┘
           │
    No ◄───┴───► Yes
    │              │
    ▼              ▼
┌────────┐   ┌──────────────────┐
│ Return │   │ Validate username│
│ Error  │   │ (length, pattern)│
└────────┘   └────────┬─────────┘
                      │
                 ┌────▼────┐
                 │ Valid?  │
                 └────┬────┘
                      │
               No ◄───┴───► Yes
               │              │
               ▼              ▼
          ┌────────┐   ┌─────────────┐
          │ Return │   │ Validate    │
          │ Error  │   │ email format│
          └────────┘   └──────┬──────┘
                              │
                         ┌────▼────┐
                         │ Valid?  │
                         └────┬────┘
                              │
                       No ◄───┴───► Yes
                       │              │
                       ▼              ▼
                  ┌────────┐   ┌─────────────┐
                  │ Return │   │ Validate    │
                  │ Error  │   │ password    │
                  └────────┘   │ length >= 8 │
                               └──────┬──────┘
                                      │
                                 ┌────▼────┐
                                 │ Valid?  │
                                 └────┬────┘
                                      │
                               No ◄───┴───► Yes
                               │              │
                               ▼              ▼
                          ┌────────┐   ┌──────────────┐
                          │ Return │   │ Check if     │
                          │ Error  │   │ username     │
                          └────────┘   │ exists in DB │
                                       └──────┬───────┘
                                              │
                                         ┌────▼────┐
                                         │ Exists? │
                                         └────┬────┘
                                              │
                                       Yes ◄──┴──► No
                                       │            │
                                       ▼            ▼
                                  ┌────────┐ ┌──────────────┐
                                  │ Return │ │ Check if     │
                                  │ Error  │ │ email exists │
                                  └────────┘ └──────┬───────┘
                                                    │
                                               ┌────▼────┐
                                               │ Exists? │
                                               └────┬────┘
                                                    │
                                             Yes ◄──┴──► No
                                             │            │
                                             ▼            ▼
                                        ┌────────┐ ┌──────────────┐
                                        │ Return │ │ Hash password│
                                        │ Error  │ │ (bcrypt, 12) │
                                        └────────┘ └──────┬───────┘
                                                          │
                                                          ▼
                                                   ┌──────────────┐
                                                   │ INSERT user  │
                                                   │ into database│
                                                   └──────┬───────┘
                                                          │
                                                     ┌────▼────┐
                                                     │Success? │
                                                     └────┬────┘
                                                          │
                                                   Yes ◄──┴──► No
                                                   │            │
                                                   ▼            ▼
                                            ┌────────────┐ ┌────────┐
                                            │ Flash msg  │ │ Return │
                                            │ Redirect   │ │ Error  │
                                            │ to /login  │ └────────┘
                                            └────────────┘
```

---

## 2. User Login Algorithm

### Purpose
Authenticate user credentials securely using constant-time password comparison.

### Pseudocode

```
ALGORITHM LoginUser(username, password, csrf_token)

INPUT:
    username: string (from form)
    password: string (from form)
    csrf_token: string (from hidden form field)

OUTPUT:
    success: create session, redirect to home
    OR
    error: re-display login form with error message

BEGIN

    // Step 1: CSRF Protection
    IF NOT validate_csrf_token(csrf_token, session['csrf_token']) THEN
        RETURN error("Invalid request. Please try again.")
    END IF

    // Step 2: Check for Empty Fields
    IF is_empty(username) OR is_empty(password) THEN
        RETURN error("Please provide both username and password.")
    END IF

    // Step 3: Retrieve User from Database
    user = database.query(
        "SELECT id, username, password_hash, created_at
         FROM users
         WHERE username = ?",
        [username]
    )

    // Step 4: Check if User Exists
    IF user IS NULL THEN
        // Generic error message (prevent username enumeration)
        log_attempt("Failed login attempt for username: " + username)
        RETURN error("Invalid username or password.")
    END IF

    // Step 5: Verify Password (Constant-Time Comparison)
    password_matches = bcrypt.check_password_hash(
        user.password_hash,
        password
    )
    // bcrypt.check_password_hash uses constant-time comparison
    // to prevent timing attacks

    // Step 6: Handle Password Verification Result
    IF NOT password_matches THEN
        // Generic error message (prevent username enumeration)
        log_attempt("Failed login attempt for user_id: " + user.id)
        RETURN error("Invalid username or password.")
    END IF

    // Step 7: Password Valid - Create Session
    session.clear()  // Clear any existing session data
    session['user_id'] = user.id
    session['username'] = user.username
    session['logged_in_at'] = current_timestamp()
    session.permanent = TRUE  // Makes session persist

    // Step 8: Set Secure Cookie Flags
    // (Configured at application level)
    // - HttpOnly: TRUE (prevents JavaScript access)
    // - SameSite: 'Lax' (CSRF protection)
    // - Secure: TRUE (HTTPS only - in production)

    // Step 9: Log Successful Login
    log_info("Successful login for user_id: " + user.id)

    // Step 10: Success Response
    flash_message("Welcome back, " + user.username + "!")
    RETURN redirect("/")

END ALGORITHM
```

### Security Properties

1. **Constant-Time Comparison**: Prevents timing attacks by taking same time regardless of password correctness
2. **Generic Error Messages**: "Invalid username or password" prevents attacker from knowing if username exists
3. **No Username Enumeration**: Same error for non-existent user and wrong password
4. **Secure Session Management**: HttpOnly cookies, SameSite protection
5. **Logging**: Failed attempts logged for security monitoring

---

## 3. Authorization Check Algorithm

### Purpose
Verify that a logged-in user has permission to modify a specific review (ownership check).

### Pseudocode

```
ALGORITHM CheckReviewOwnership(user_id, review_id)

INPUT:
    user_id: integer (from session)
    review_id: integer (from URL parameter)

OUTPUT:
    authorized: TRUE (allow operation)
    OR
    error: 403 Forbidden

BEGIN

    // Step 1: Check if User is Logged In
    IF user_id IS NULL THEN
        log_warning("Unauthorized access attempt to review_id: " + review_id)
        RETURN 403_error("You must be logged in to perform this action.")
    END IF

    // Step 2: Validate Review ID
    IF NOT is_integer(review_id) OR review_id <= 0 THEN
        log_warning("Invalid review_id provided: " + review_id)
        RETURN 400_error("Invalid review ID.")
    END IF

    // Step 3: Retrieve Review from Database
    review = database.query(
        "SELECT id, user_id, title
         FROM reviews
         WHERE id = ?",
        [review_id]
    )

    // Step 4: Check if Review Exists
    IF review IS NULL THEN
        log_info("Review not found: " + review_id)
        RETURN 404_error("Review not found.")
    END IF

    // Step 5: Verify Ownership
    IF review.user_id != user_id THEN
        log_warning(
            "User " + user_id + " attempted to access review " +
            review_id + " owned by user " + review.user_id
        )
        RETURN 403_error(
            "You do not have permission to modify this review."
        )
    END IF

    // Step 6: Authorization Successful
    log_info("Authorization granted: user " + user_id + " accessing review " + review_id)
    RETURN authorized(TRUE)

END ALGORITHM
```

### Flowchart

```
┌─────────────────────┐
│  Start: User         │
│  attempts to edit    │
│  or delete review    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Check if user is   │
│  logged in (session)│
└──────────┬──────────┘
           │
      ┌────▼────┐
      │Logged in│
      └────┬────┘
           │
    No ◄───┴───► Yes
    │              │
    ▼              ▼
┌─────────┐  ┌──────────────────┐
│ Redirect│  │ Query database   │
│ to login│  │ for review by ID │
└─────────┘  └────────┬─────────┘
                      │
                 ┌────▼────┐
                 │ Review  │
                 │ exists? │
                 └────┬────┘
                      │
               No ◄───┴───► Yes
               │              │
               ▼              ▼
          ┌─────────┐  ┌──────────────────┐
          │ Return  │  │ Compare:         │
          │ 404     │  │ session[user_id] │
          │ Error   │  │ ==               │
          └─────────┘  │ review.user_id   │
                       └────────┬─────────┘
                                │
                           ┌────▼────┐
                           │ Match?  │
                           └────┬────┘
                                │
                         No ◄───┴───► Yes
                         │              │
                         ▼              ▼
                    ┌─────────┐  ┌──────────────┐
                    │ Return  │  │ Authorization│
                    │ 403     │  │ granted!     │
                    │ Error   │  │ Allow edit/  │
                    └─────────┘  │ delete       │
                                 └──────────────┘
```

---

## 4. XSS Prevention Algorithm

### Purpose
Sanitize user inputs to prevent Cross-Site Scripting attacks.

### Pseudocode

```
ALGORITHM SanitizeUserInput(raw_input)

INPUT:
    raw_input: string (from user form submission)

OUTPUT:
    sanitized_input: string (safe for storage and display)

BEGIN

    // Step 1: HTML Entity Encoding
    // Convert dangerous characters to HTML entities
    sanitized_input = raw_input

    // Replace < with &lt;
    sanitized_input = replace(sanitized_input, "<", "&lt;")

    // Replace > with &gt;
    sanitized_input = replace(sanitized_input, ">", "&gt;")

    // Replace & with &amp; (must be done carefully to avoid double-encoding)
    sanitized_input = replace(sanitized_input, "&", "&amp;")

    // Replace " with &quot;
    sanitized_input = replace(sanitized_input, '"', "&quot;")

    // Replace ' with &#x27;
    sanitized_input = replace(sanitized_input, "'", "&#x27;")

    // Step 2: Remove Null Bytes (can cause issues)
    sanitized_input = replace(sanitized_input, "\0", "")

    // Step 3: Trim Whitespace
    sanitized_input = trim(sanitized_input)

    // Step 4: Log if Suspicious Input Detected
    IF contains(raw_input, "<script") OR
       contains(raw_input, "javascript:") OR
       contains(raw_input, "onerror=") OR
       contains(raw_input, "onclick=") THEN
        log_warning("Potential XSS attempt detected: " + raw_input)
    END IF

    RETURN sanitized_input

END ALGORITHM
```

### Example

```
INPUT:  <script>alert('XSS')</script>
OUTPUT: &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;

INPUT:  <img src=x onerror=alert('XSS')>
OUTPUT: &lt;img src=x onerror=alert(&#x27;XSS&#x27;)&gt;

INPUT:  Normal review text
OUTPUT: Normal review text
```

### Template Layer Protection (Jinja2)

```
TEMPLATE RENDERING WITH AUTO-ESCAPING

In templates, Jinja2 auto-escaping is ENABLED by default:

{{ user_input }}  <-- Automatically escaped
{{ user_input | safe }}  <-- NOT escaped (dangerous, avoid)
{{ user_input | e }}  <-- Explicitly escaped (redundant but safe)

Example:
user_input = "<script>alert('xss')</script>"

Template: <p>{{ user_input }}</p>
Rendered: <p>&lt;script&gt;alert('xss')&lt;/script&gt;</p>

Browser displays: <script>alert('xss')</script> as TEXT, not executed
```

---

## 5. CSRF Protection Algorithm

### Purpose
Generate and validate CSRF tokens to prevent Cross-Site Request Forgery attacks.

### Pseudocode

```
ALGORITHM GenerateCSRFToken()

OUTPUT:
    csrf_token: string (cryptographically secure random token)

BEGIN

    // Step 1: Generate Random Token
    // Use cryptographically secure random number generator
    random_bytes = generate_secure_random_bytes(32)  // 32 bytes = 256 bits

    // Step 2: Encode as Hexadecimal
    csrf_token = encode_hex(random_bytes)  // Results in 64 character hex string

    // Step 3: Store in Session
    session['csrf_token'] = csrf_token

    // Step 4: Set Timestamp (Optional, for expiration)
    session['csrf_token_time'] = current_timestamp()

    RETURN csrf_token

END ALGORITHM


ALGORITHM ValidateCSRFToken(submitted_token)

INPUT:
    submitted_token: string (from form hidden field)

OUTPUT:
    valid: boolean (TRUE if token is valid, FALSE otherwise)

BEGIN

    // Step 1: Check if Token Exists in Session
    IF 'csrf_token' NOT IN session THEN
        log_warning("CSRF token missing from session")
        RETURN FALSE
    END IF

    session_token = session['csrf_token']

    // Step 2: Check if Submitted Token is Empty
    IF is_empty(submitted_token) THEN
        log_warning("Empty CSRF token submitted")
        RETURN FALSE
    END IF

    // Step 3: Constant-Time Comparison
    // Prevents timing attacks
    IF NOT constant_time_compare(submitted_token, session_token) THEN
        log_warning("CSRF token mismatch")
        log_info("Expected: " + session_token[0:10] + "...")
        log_info("Received: " + submitted_token[0:10] + "...")
        RETURN FALSE
    END IF

    // Step 4: Check Token Age (Optional)
    IF 'csrf_token_time' IN session THEN
        token_age = current_timestamp() - session['csrf_token_time']
        MAX_TOKEN_AGE = 3600  // 1 hour in seconds

        IF token_age > MAX_TOKEN_AGE THEN
            log_info("CSRF token expired (age: " + token_age + " seconds)")
            RETURN FALSE
        END IF
    END IF

    // Step 5: Token Valid
    RETURN TRUE

END ALGORITHM
```

### Implementation in Forms

```html
<!-- In HTML forms -->
<form method="POST" action="/reviews/create">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">

    <!-- Other form fields -->

    <button type="submit">Submit</button>
</form>
```

### Implementation in Routes

```python
@app.route('/reviews/create', methods=['POST'])
@login_required
def create_review():
    # Validate CSRF token
    if not validate_csrf_token(request.form.get('csrf_token')):
        return abort(403, "Invalid CSRF token")

    # Process form...
```

---

## 6. SQL Injection Prevention Algorithm

### Purpose
Use parameterized queries to prevent SQL injection attacks.

### UNSAFE Example (Vulnerable to SQL Injection)

```
DANGEROUS CODE - DO NOT USE:

username = request.form['username']
password = request.form['password']

// String concatenation - VULNERABLE!
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
user = database.execute(query)

// Attack example:
// username = "admin' --"
// password = "anything"
//
// Resulting query:
// SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'
//                                           ^^ Comment out rest of query
// Attacker logs in as admin without knowing password!
```

### SAFE Algorithm (Parameterized Queries)

```
ALGORITHM SafeDatabaseQuery(query_template, parameters)

INPUT:
    query_template: string with ? placeholders
    parameters: array of values

OUTPUT:
    result: database result set

BEGIN

    // Step 1: Prepare Statement
    // Database driver handles escaping automatically
    prepared_statement = database.prepare(query_template)

    // Step 2: Bind Parameters
    // Each ? is replaced with properly escaped value
    FOR i = 0 TO length(parameters) - 1 DO
        prepared_statement.bind_parameter(i, parameters[i])
    END FOR

    // Step 3: Execute Query
    result = prepared_statement.execute()

    // Step 4: Return Result
    RETURN result

END ALGORITHM


EXAMPLE USAGE:

// Safe login query
username = request.form['username']
password = request.form['password']

user = database.query(
    "SELECT id, username, password_hash FROM users WHERE username = ?",
    [username]
)

// Even if username = "admin' --", it's treated as literal string
// The query becomes:
// SELECT id, username, password_hash FROM users WHERE username = 'admin\' --'
//                                                                      ^^ Escaped
// No SQL injection possible!


// Safe insert review
database.execute(
    "INSERT INTO reviews (user_id, title, review_text, rating, category)
     VALUES (?, ?, ?, ?, ?)",
    [user_id, title, review_text, rating, category]
)

// All special characters in values are automatically escaped
```

### Additional SQL Safety Rules

1. **Never concatenate user input into SQL strings**
2. **Always use ? placeholders for SQLite** (or %s for MySQL, $1 for PostgreSQL)
3. **Validate data types**: Ensure integers are integers before querying
4. **Use ORM when possible**: SQLAlchemy provides additional abstraction
5. **Least privilege**: Database user should have minimum required permissions

---

## 7. Session Security Algorithm

### Purpose
Configure secure session management to prevent session hijacking.

### Pseudocode

```
ALGORITHM ConfigureSecureSession(app)

INPUT:
    app: Flask application instance

OUTPUT:
    configured app with secure session settings

BEGIN

    // Step 1: Secret Key (for signing session cookies)
    // Must be cryptographically random and kept secret
    app.config['SECRET_KEY'] = load_from_environment('SECRET_KEY')

    IF is_empty(app.config['SECRET_KEY']) THEN
        RAISE error("SECRET_KEY must be set in environment variables")
    END IF

    // Step 2: Session Cookie Name
    app.config['SESSION_COOKIE_NAME'] = 'review_app_session'

    // Step 3: HttpOnly Flag
    // Prevents JavaScript from accessing cookie (XSS protection)
    app.config['SESSION_COOKIE_HTTPONLY'] = TRUE

    // Step 4: Secure Flag
    // Ensures cookie only sent over HTTPS (man-in-the-middle protection)
    IF app.config['ENV'] == 'production' THEN
        app.config['SESSION_COOKIE_SECURE'] = TRUE
    ELSE
        app.config['SESSION_COOKIE_SECURE'] = FALSE  // Allow HTTP in dev
    END IF

    // Step 5: SameSite Flag
    // Prevents cookie from being sent in cross-site requests (CSRF protection)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    // Options: 'Strict', 'Lax', 'None'
    // Lax = Sent with GET requests, not POST from other sites

    // Step 6: Session Lifetime
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  // 1 hour in seconds

    // Step 7: Session Regeneration (on login)
    // Prevents session fixation attacks
    FUNCTION on_user_login(user_id):
        old_session_data = copy(session)
        session.clear()  // Destroy old session
        session.regenerate()  // Generate new session ID
        session['user_id'] = user_id  // Restore necessary data
        session['logged_in_at'] = current_timestamp()
    END FUNCTION

    RETURN app

END ALGORITHM
```

---

## 8. Password Strength Validation (Client-Side)

### Purpose
Provide real-time feedback on password strength to users (UX enhancement, not security).

### Pseudocode

```
ALGORITHM CalculatePasswordStrength(password)

INPUT:
    password: string (as user types)

OUTPUT:
    strength: integer (0-4, where 4 is strongest)
    feedback: string (message to display)

BEGIN

    strength = 0
    feedback = ""

    // Criterion 1: Length
    IF length(password) >= 8 THEN
        strength = strength + 1
    END IF

    IF length(password) >= 12 THEN
        strength = strength + 1
    END IF

    // Criterion 2: Lowercase letters
    IF contains_lowercase(password) THEN
        strength = strength + 1
    END IF

    // Criterion 3: Uppercase letters
    IF contains_uppercase(password) THEN
        strength = strength + 1
    END IF

    // Criterion 4: Numbers
    IF contains_digit(password) THEN
        strength = strength + 1
    END IF

    // Criterion 5: Special characters
    IF contains_special_char(password) THEN
        strength = strength + 1
    END IF

    // Normalize to 0-4 scale
    strength = min(strength, 4)

    // Generate feedback
    SWITCH strength
        CASE 0:
            feedback = "Very Weak"
            color = "red"
        CASE 1:
            feedback = "Weak"
            color = "orange"
        CASE 2:
            feedback = "Fair"
            color = "yellow"
        CASE 3:
            feedback = "Good"
            color = "lightgreen"
        CASE 4:
            feedback = "Strong"
            color = "green"
    END SWITCH

    RETURN (strength, feedback, color)

END ALGORITHM
```

---

## Security Checklist

### Before Deployment

- [ ] All passwords hashed with bcrypt (12 rounds)
- [ ] CSRF tokens implemented on all forms
- [ ] XSS protection: Jinja2 auto-escaping enabled
- [ ] SQL injection: All queries use parameterized statements
- [ ] Authorization: Ownership checks on edit/delete
- [ ] Session cookies: HttpOnly, SameSite, Secure (production)
- [ ] SECRET_KEY: Strong, random, kept secret
- [ ] Input validation: Server-side validation on all inputs
- [ ] Error messages: Generic (no information leakage)
- [ ] HTTPS enabled in production
- [ ] Security headers: CSP, X-Frame-Options, X-Content-Type-Options
- [ ] Logging: Security events logged (failed logins, unauthorized access)
- [ ] Dependencies: Up to date, no known vulnerabilities

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-29 | Development Team | Initial security algorithms |
