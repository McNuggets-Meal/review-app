# Movie & Game Review PWA

A secure Progressive Web Application for reviewing movies and games, built with Flask, SQLite, and vanilla JavaScript. This project demonstrates Agile development methodology with comprehensive security features.

## 📋 Project Status

### ✅ Completed Components

#### Documentation (100% Complete)
All Agile documentation has been created in the `docs/` folder:
- ✅ `01_requirements.md` - Functional/non-functional requirements, user stories
- ✅ `02_ipo_chart.md` - Input-Process-Output charts for all major functions
- ✅ `03_storyboard.md` - User flow diagrams and wireframes
- ✅ `04_data_dictionary.md` - Complete database field specifications
- ✅ `05_uml_diagrams.md` - Class diagrams and sequence diagrams
- ✅ `06_security_algorithms.md` - Pseudocode for all security-critical operations

#### Backend (100% Complete)
All Python backend code has been implemented:
- ✅ **Config:** `config.py` with all security settings
- ✅ **Database:** `database/schema.sql`, `init_db.py`, `seed_data.py`
- ✅ **Utils:** `utils/security.py` (bcrypt hashing), `utils/validators.py`
- ✅ **Models:** `models/user.py`, `models/review.py`
- ✅ **Middleware:** `middleware/auth_required.py`, `middleware/csrf.py`
- ✅ **Routes:** `routes/auth.py`, `routes/reviews.py`, `routes/main.py`
- ✅ **App:** `app.py` (main Flask application)

#### Project Setup (100% Complete)
- ✅ `requirements.txt` - All Python dependencies
- ✅ `.gitignore` - Proper exclusions
- ✅ Directory structure created

### 🔨 Remaining Components

#### Templates (Partially Complete)
- ✅ `templates/base.html` - Base template with navigation
- ⏳ `templates/index.html` - Home page
- ⏳ `templates/auth/login.html` - Login form
- ⏳ `templates/auth/register.html` - Registration form
- ⏳ `templates/reviews/create.html` - Create review form
- ⏳ `templates/reviews/edit.html` - Edit review form
- ⏳ `templates/reviews/view.html` - Single review view
- ⏳ `templates/reviews/my_reviews.html` - User's reviews
- ⏳ `templates/errors/404.html`, `403.html`, `500.html` - Error pages

#### Static Files (Not Started)
- ⏳ `static/css/main.css` - Main styles
- ⏳ `static/css/auth.css` - Auth page styles
- ⏳ `static/css/reviews.css` - Review styles
- ⏳ `static/js/app.js` - Service worker registration
- ⏳ `static/js/auth.js` - Form validation
- ⏳ `static/js/reviews.js` - Review interactions
- ⏳ `static/manifest.json` - PWA manifest
- ⏳ `static/js/service-worker.js` - Offline functionality
- ⏳ `static/images/icons/` - PWA icons (8 sizes)

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

#### 1. Install Dependencies
```bash
cd review-app
pip install -r requirements.txt
```

#### 2. Initialize Database
```bash
python database/init_db.py
```

#### 3. Seed Sample Data
```bash
python database/seed_data.py
```

This creates:
- **3 Users:**
  - `john_doe` / `SecurePass123!`
  - `jane_smith` / `JaneSecure456!`
  - `alex_wong` / `AlexPass789!`
- **5-8 Movies/Games:** The Matrix, Inception, Elden Ring, Hollow Knight, etc.
- **15+ Reviews:** Multiple reviews from different users

#### 4. Run Application
```bash
python app.py
```

Visit: http://localhost:5000

---

## 🏗️ Architecture Overview

### Technology Stack
- **Backend:** Python 3.x + Flask 3.0.0
- **Database:** SQLite3 with foreign key constraints
- **Security:** bcrypt password hashing (12 rounds)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
- **PWA:** Service Worker API, Web App Manifest

### Database Schema

**users table:**
- id (PK), username (UNIQUE), email (UNIQUE), password_hash, created_at

**reviews table:**
- id (PK), user_id (FK→users.id), title, review_text, rating (1-5)
- review_date, updated_at, category (movie/game)

**Relationship:** One user → Many reviews (CASCADE DELETE)

### Security Features

#### 1. Password Security
- ✅ Bcrypt hashing with 12 rounds
- ✅ Passwords never stored in plaintext
- ✅ Constant-time comparison (prevents timing attacks)

#### 2. CSRF Protection
- ✅ Token generation per session
- ✅ Validation on all POST/PUT/DELETE requests
- ✅ Hidden tokens in all forms

#### 3. XSS Prevention
- ✅ Jinja2 auto-escaping enabled
- ✅ Input sanitization (HTML entity encoding)
- ✅ Content Security Policy headers

#### 4. SQL Injection Prevention
- ✅ Parameterized queries exclusively
- ✅ No string concatenation in SQL

#### 5. Authorization
- ✅ @login_required decorator
- ✅ Ownership verification (users can only edit their own reviews)
- ✅ 403 Forbidden for unauthorized access

#### 6. Session Security
- ✅ HttpOnly cookies (prevents JavaScript access)
- ✅ SameSite='Lax' (CSRF protection)
- ✅ Secure flag for production (HTTPS only)

---

## 📁 Project Structure

```
review-app/
├── docs/                          # Agile documentation
│   ├── 01_requirements.md
│   ├── 02_ipo_chart.md
│   ├── 03_storyboard.md
│   ├── 04_data_dictionary.md
│   ├── 05_uml_diagrams.md
│   └── 06_security_algorithms.md
├── database/
│   ├── schema.sql                 # Database schema
│   ├── init_db.py                 # Initialize database
│   └── seed_data.py               # Sample data
├── models/
│   ├── user.py                    # User database operations
│   └── review.py                  # Review database operations
├── routes/
│   ├── auth.py                    # Register, login, logout
│   ├── reviews.py                 # CRUD operations
│   └── main.py                    # Home page
├── middleware/
│   ├── auth_required.py           # Login protection
│   └── csrf.py                    # CSRF tokens
├── utils/
│   ├── security.py                # Password hashing
│   └── validators.py              # Input validation
├── templates/                     # Jinja2 templates
│   ├── base.html                  # ✅ Base layout
│   ├── index.html                 # ⏳ Home page
│   ├── auth/                      # ⏳ Auth templates
│   └── reviews/                   # ⏳ Review templates
├── static/                        # ⏳ CSS, JS, PWA assets
├── app.py                         # ✅ Main Flask app
├── config.py                      # ✅ Configuration
├── requirements.txt               # ✅ Dependencies
└── .gitignore                     # ✅ Git exclusions
```

---

## 🎯 Implementation Guide for Remaining Files

### Templates

Each template should:
1. Extend `base.html`
2. Override the `{% block content %}` section
3. Include CSRF tokens in forms: `<input type="hidden" name="csrf_token" value="{{ csrf_token }}">`
4. Use Jinja2 auto-escaping: `{{ variable }}` (automatically escaped)

**Example template pattern:**
```html
{% extends 'base.html' %}
{% block title %}Page Title{% endblock %}
{% block content %}
<h1>Content Here</h1>
{% endblock %}
```

### CSS Files

**main.css** should include:
- CSS variables for theming (colors, fonts)
- Responsive grid layout (mobile-first)
- Navigation bar styles
- Card layouts for reviews
- Star rating display
- Alert/flash message styles
- Form styles

**Responsive breakpoints:**
- Mobile: 320px-767px (single column)
- Tablet: 768px-1023px (two columns)
- Desktop: 1024px+ (three columns, max-width 1200px)

### JavaScript Files

**app.js** - PWA initialization:
```javascript
// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/js/service-worker.js');
}
```

**auth.js** - Form validation:
- Password strength indicator
- Email format validation
- Client-side validation (UX, not security)

**reviews.js** - Interactive features:
- Star rating UI (clickable stars)
- Character counter for review text
- Delete confirmation dialog

### PWA Files

**manifest.json:**
```json
{
  "name": "Movie & Game Reviews",
  "short_name": "Reviews",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#007bff",
  "icons": [...]
}
```

**service-worker.js:**
- Cache static assets on install
- Serve from cache first
- Fall back to network
- Clean old caches

**Icons needed:**
- 72x72, 96x96, 128x128, 144x144, 152x152, 192x192, 384x384, 512x512px

---

## 🧪 Testing Checklist

### Functional Tests
- [ ] User registration creates account
- [ ] User login creates session
- [ ] Logout clears session
- [ ] Create review (logged-in only)
- [ ] Edit own review (ownership check)
- [ ] Delete own review (ownership check)
- [ ] Cannot edit others' reviews (403)
- [ ] View all reviews (public)
- [ ] Filter by category/rating

### Security Tests
- [ ] Passwords hashed in database (not plaintext)
- [ ] XSS: Input `<script>alert('xss')</script>` → escaped
- [ ] CSRF: POST without token → rejected
- [ ] SQL Injection: Input `' OR '1'='1` → no bypass
- [ ] Authorization: User A cannot modify User B's review

### PWA Tests
- [ ] Service worker registers
- [ ] App installable
- [ ] Offline mode works
- [ ] Lighthouse PWA score > 90

---

## 🔒 Security Configuration

### Production Deployment

**IMPORTANT:** Before deploying to production:

1. **Change SECRET_KEY:**
   ```python
   # In config.py or environment variable
   SECRET_KEY = 'your-cryptographically-secure-random-key-here'
   ```
   Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

2. **Enable HTTPS:**
   ```python
   SESSION_COOKIE_SECURE = True
   ```

3. **Update CSP headers** in `config.py` if needed

4. **Disable debug mode:**
   ```python
   # In app.py
   app.run(debug=False)
   ```

---

## 📚 Additional Resources

### Documentation
All comprehensive Agile documentation is in the `docs/` folder:
- Requirements analysis
- User stories with acceptance criteria
- IPO charts for all major functions
- UML diagrams (class and sequence)
- Security algorithm pseudocode
- Complete data dictionary

### Git Workflow

```bash
# Initialize repository
cd review-app
git init

# Initial commit
git add .
git commit -m "Initial commit: Complete backend + documentation

- Agile documentation (6 files)
- Flask backend with security features
- SQLite database with sample data
- Bcrypt password hashing
- CSRF protection
- XSS prevention
- Authorization checks

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/review-app.git
git push -u origin main
```

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Agile development methodology
- ✅ Secure password storage (bcrypt)
- ✅ CSRF attack prevention
- ✅ XSS attack prevention
- ✅ SQL injection prevention
- ✅ Session management
- ✅ Authorization and authentication
- ✅ RESTful API design
- ✅ Database relationships (foreign keys)
- ✅ MVC architecture pattern
- ✅ Progressive Web App concepts

---

## 📝 License

Educational project for St Edwards College.

---

## 🤝 Contributing

This is an educational assessment project. Please complete the remaining frontend files following the patterns established in the backend code.

---

## 💡 Tips for Completion

1. **Start with templates:** Create `index.html` to display reviews
2. **Then auth templates:** `login.html` and `register.html`
3. **Review templates:** `create.html`, `edit.html`, `view.html`, `my_reviews.html`
4. **Style incrementally:** Start with `main.css`, test as you go
5. **Add interactivity:** JavaScript for star ratings, form validation
6. **Finish with PWA:** Manifest, service worker, icons

---

## ✨ Features Implemented

### Core Features
- ✅ User registration with validation
- ✅ Secure login (bcrypt)
- ✅ Session management
- ✅ Create reviews (protected)
- ✅ Edit own reviews (ownership check)
- ✅ Delete own reviews (ownership check)
- ✅ View all reviews (public)
- ✅ Filter by category/rating
- ✅ View single review detail

### Security Features
- ✅ Password hashing (bcrypt, 12 rounds)
- ✅ CSRF protection
- ✅ XSS prevention (Jinja2 auto-escaping)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Authorization checks
- ✅ Secure session cookies
- ✅ Security headers (CSP, X-Frame-Options, etc.)

### Database Features
- ✅ Foreign key relationships
- ✅ Check constraints (rating 1-5, category validation)
- ✅ Indexes for performance
- ✅ CASCADE DELETE (user deletion deletes reviews)
- ✅ Sample data (3 users, 15+ reviews, 8 movies/games)

---

## 📞 Support

For questions or issues:
1. Review the documentation in `docs/` folder
2. Check the code comments in backend files
3. Refer to the security algorithms document for implementation details

---

**Project Status:** Backend Complete | Frontend In Progress | Ready for Template Development

Generated with assistance from Claude Code (Anthropic)
