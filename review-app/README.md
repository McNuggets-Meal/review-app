# Movie & Game Review PWA

A secure Progressive Web Application for reviewing movies and games, built with Flask, SQLite, and vanilla JavaScript. This project demonstrates Agile development methodology with comprehensive security features.

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

- **3 Users:**
  - `john_doe` / `SecurePass123!`
  - `jane_smith` / `JaneSecure456!`
  - `alex_wong` / `AlexPass789!`
- **15+ Reviews:** Multiple reviews from different users

#### 4. Run Application
```bash
python app.py
```

Visit: http://localhost:5000

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
