# Project Requirements Document
## Movie & Game Review PWA

### Project Overview
A Progressive Web Application that allows users to register accounts, login securely, and post reviews for movies and games. The application emphasizes security through password hashing, XSS protection, CSRF protection, and proper authorization controls.

---

## 1. Functional Requirements

### FR1: User Registration
**Description:** New users can create accounts with username, email, and password.
- **Input:** Username (3-50 characters), valid email, password (minimum 8 characters)
- **Process:** Validate inputs, check for duplicates, hash password with bcrypt, insert into database
- **Output:** Account created successfully or error message
- **Priority:** High

### FR2: User Login
**Description:** Registered users can authenticate with their credentials.
- **Input:** Username and password
- **Process:** Verify credentials against database, create secure session
- **Output:** Redirect to home page or display error message
- **Priority:** High

### FR3: User Logout
**Description:** Logged-in users can terminate their session.
- **Input:** Logout button click
- **Process:** Clear session data
- **Output:** Redirect to home page with confirmation
- **Priority:** High

### FR4: Create Review
**Description:** Authenticated users can post new reviews.
- **Input:** Movie/game title, category (movie/game), rating (1-5 stars), review text
- **Process:** Validate inputs, associate with user_id, insert into database
- **Output:** Review published or error message
- **Priority:** High
- **Authorization:** Requires logged-in user

### FR5: View All Reviews
**Description:** All visitors (logged in or not) can view published reviews.
- **Input:** Optional filters (category, rating)
- **Process:** Query database, format results
- **Output:** Display list of reviews with title, rating, excerpt, author, date
- **Priority:** High
- **Authorization:** Public access

### FR6: View Single Review
**Description:** Display full details of a specific review.
- **Input:** Review ID
- **Process:** Query database for review details
- **Output:** Full review with all fields
- **Priority:** Medium
- **Authorization:** Public access

### FR7: Edit Review
**Description:** Users can modify their own reviews.
- **Input:** Review ID and updated fields
- **Process:** Verify ownership, validate inputs, update database
- **Output:** Review updated successfully or error message
- **Priority:** High
- **Authorization:** Requires logged-in user + ownership verification

### FR8: Delete Review
**Description:** Users can delete their own reviews.
- **Input:** Review ID
- **Process:** Verify ownership, delete from database
- **Output:** Review deleted or error message
- **Priority:** High
- **Authorization:** Requires logged-in user + ownership verification

### FR9: View My Reviews
**Description:** Users can see a list of all their own reviews.
- **Input:** User session
- **Process:** Query reviews by user_id
- **Output:** List of user's reviews with edit/delete options
- **Priority:** Medium
- **Authorization:** Requires logged-in user

### FR10: Filter/Search Reviews
**Description:** Users can filter reviews by category or rating.
- **Input:** Filter criteria (category: movie/game, rating: 1-5)
- **Process:** Query database with filter parameters
- **Output:** Filtered list of reviews
- **Priority:** Low

---

## 2. Non-Functional Requirements

### NFR1: Security - Password Storage
**Description:** User passwords must be securely hashed using bcrypt with 12 rounds.
- **Acceptance:** No plaintext passwords stored in database
- **Verification:** Database inspection shows only hashed passwords
- **Priority:** Critical

### NFR2: Security - XSS Protection
**Description:** All user inputs must be properly escaped to prevent Cross-Site Scripting attacks.
- **Acceptance:** Malicious scripts in input do not execute
- **Implementation:** Jinja2 auto-escaping, Content Security Policy headers
- **Verification:** Test inputs like `<script>alert('XSS')</script>` are rendered as text
- **Priority:** Critical

### NFR3: Security - CSRF Protection
**Description:** All state-changing operations must include CSRF token validation.
- **Acceptance:** POST/PUT/DELETE requests without valid token are rejected
- **Implementation:** Token generation and validation middleware
- **Priority:** Critical

### NFR4: Security - SQL Injection Prevention
**Description:** All database queries must use parameterized statements.
- **Acceptance:** SQL injection attempts fail
- **Implementation:** Parameterized queries with ? placeholders
- **Verification:** Test inputs like `' OR '1'='1` do not bypass security
- **Priority:** Critical

### NFR5: Security - Authorization
**Description:** Users can only modify their own reviews.
- **Acceptance:** Attempts to edit/delete others' reviews return 403 Forbidden
- **Implementation:** Ownership verification before update/delete operations
- **Priority:** Critical

### NFR6: Performance - Response Time
**Description:** Page load times should be under 2 seconds on standard connection.
- **Acceptance:** 95% of requests complete within 2 seconds
- **Implementation:** Optimized queries, caching, minimized assets
- **Priority:** Medium

### NFR7: Usability - Responsive Design
**Description:** Application must be fully functional on mobile, tablet, and desktop.
- **Acceptance:** UI adapts to screen sizes from 320px to 1920px
- **Implementation:** Mobile-first CSS, flexible layouts
- **Priority:** High

### NFR8: Availability - PWA Offline Mode
**Description:** Core content should be accessible offline after initial visit.
- **Acceptance:** Cached pages load without internet connection
- **Implementation:** Service worker with cache-first strategy
- **Priority:** Medium

### NFR9: Accessibility - WCAG Compliance
**Description:** Application should meet WCAG 2.1 AA standards.
- **Acceptance:** Screen reader compatible, keyboard navigable, sufficient contrast
- **Implementation:** Semantic HTML, ARIA labels, focus states
- **Priority:** Medium

### NFR10: Compatibility - Browser Support
**Description:** Support modern browsers (Chrome, Firefox, Safari, Edge).
- **Acceptance:** Full functionality on browsers with <2% market share
- **Implementation:** Standard web APIs, progressive enhancement
- **Priority:** Medium

---

## 3. User Stories with Acceptance Criteria

### Epic 1: User Authentication

#### US-1: User Registration
**As a** new user
**I want to** create an account
**So that** I can post reviews

**Acceptance Criteria:**
- Given I am on the registration page
- When I enter valid username, email, and password
- Then my account is created and I am redirected to login
- And my password is hashed with bcrypt in the database
- And I cannot use an already-taken username or email

#### US-2: User Login
**As a** registered user
**I want to** log into my account
**So that** I can manage my reviews

**Acceptance Criteria:**
- Given I have a registered account
- When I enter correct username and password
- Then I am logged in and redirected to home page
- And my session persists across page navigation
- And incorrect credentials show generic error message

#### US-3: User Logout
**As a** logged-in user
**I want to** log out of my account
**So that** others cannot access my account

**Acceptance Criteria:**
- Given I am logged in
- When I click the logout button
- Then my session is cleared
- And I am redirected to home page
- And I cannot access protected pages without logging in again

### Epic 2: Review Management

#### US-4: Create Review
**As a** logged-in user
**I want to** create a new review
**So that** I can share my opinion about movies/games

**Acceptance Criteria:**
- Given I am logged in
- When I fill the review form with valid data
- Then my review is saved with my username
- And appears on the public reviews page
- And non-logged-in users are redirected to login

#### US-5: Edit My Review
**As a** logged-in user
**I want to** edit my existing reviews
**So that** I can update or correct my opinions

**Acceptance Criteria:**
- Given I am logged in and viewing my review
- When I click edit and modify fields
- Then my review is updated successfully
- And the updated_at timestamp is changed
- And I cannot edit other users' reviews (403 error)

#### US-6: Delete My Review
**As a** logged-in user
**I want to** delete my reviews
**So that** I can remove content I no longer want published

**Acceptance Criteria:**
- Given I am logged in and viewing my review
- When I click delete and confirm
- Then my review is permanently removed
- And I cannot delete other users' reviews (403 error)
- And deleted reviews no longer appear on public pages

### Epic 3: Public Viewing

#### US-7: View All Reviews
**As a** visitor (logged in or not)
**I want to** see all published reviews
**So that** I can discover opinions about movies and games

**Acceptance Criteria:**
- Given I visit the home page
- When the page loads
- Then I see all reviews sorted by most recent
- And each review shows title, rating, excerpt, author, date
- And I can filter by category (movie/game) or rating

#### US-8: View Single Review
**As a** visitor
**I want to** view full review details
**So that** I can read complete opinions

**Acceptance Criteria:**
- Given I click on a review card
- When the detail page loads
- Then I see title, rating, full text, author, and date
- And if I'm the author, I see edit/delete buttons
- And if I'm not the author, edit/delete buttons are hidden

### Epic 4: Progressive Web App

#### US-9: Install as App
**As a** user
**I want to** install the app to my device
**So that** I can access it like a native application

**Acceptance Criteria:**
- Given I am using a PWA-compatible browser
- When I visit the site
- Then I see an install prompt (if eligible)
- And I can install to home screen
- And the app opens in standalone mode (no browser UI)

#### US-10: Offline Access
**As a** user
**I want to** view cached content offline
**So that** I can read reviews without internet connection

**Acceptance Criteria:**
- Given I have visited the app while online
- When I lose internet connection
- Then I can still view cached pages
- And I see an indicator that I'm offline
- And I cannot create/edit reviews while offline

---

## 4. Constraints

### C1: Technology Stack
- Backend: Python Flask
- Database: SQLite
- Frontend: HTML, CSS, JavaScript (vanilla, no frameworks required)
- No external authentication services (OAuth, Auth0, etc.)

### C2: Development Environment
- Must work on Windows development environment
- Must use Git for version control (GitHub recommended)
- Must be testable on localhost

### C3: Browser Compatibility
- Must support modern browsers with service worker support
- PWA features may not work on all browsers (acceptable degradation)

### C4: Database Constraints
- Single SQLite database file
- No database server required
- Foreign key constraints must be enabled

### C5: No Third-Party APIs
- No integration with TMDB, IGDB, or other external movie/game APIs
- All content manually entered by users

---

## 5. Acceptance Criteria (Project-Level)

### Documentation Complete
- [ ] All 6 planning documents created (requirements, IPO, storyboard, data dictionary, UML, security algorithms)
- [ ] Documents follow Agile methodology
- [ ] Clear user stories with acceptance criteria

### Functional Complete
- [ ] Users can register, login, and logout
- [ ] Logged-in users can create, edit, and delete their own reviews
- [ ] All users can view all published reviews
- [ ] Authorization prevents unauthorized modifications

### Security Complete
- [ ] Passwords hashed with bcrypt (verified in database)
- [ ] XSS protection verified (malicious scripts escaped)
- [ ] CSRF protection implemented (tokens in all forms)
- [ ] SQL injection prevented (parameterized queries)
- [ ] Authorization enforced (ownership checks)

### Database Complete
- [ ] SQLite database with users and reviews tables
- [ ] Foreign key relationship (reviews.user_id → users.id)
- [ ] Check constraints (rating 1-5, category movie/game)
- [ ] 3 sample users with hashed passwords
- [ ] 5-8 sample movies/games
- [ ] 12+ sample reviews

### PWA Complete
- [ ] manifest.json with app metadata and icons
- [ ] Service worker caching static assets
- [ ] App installable to home screen
- [ ] Offline mode works (cached content accessible)
- [ ] Lighthouse PWA score > 90

### Code Quality
- [ ] Git repository initialized with clean history
- [ ] .gitignore excludes database, __pycache__, venv
- [ ] Code follows PEP 8 (Python) conventions
- [ ] Clear file organization (models, routes, templates, static)
- [ ] README with setup instructions

### User Experience
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Clear navigation and error messages
- [ ] Accessible (keyboard navigation, screen reader friendly)
- [ ] Flash messages for user feedback
- [ ] Star rating visual display

---

## 6. Assumptions

1. Users have Python 3.7+ installed
2. Users understand basic web application concepts
3. All reviews are in English
4. No content moderation required (trusted users)
5. No user profile pictures or avatars
6. No email verification required for registration
7. No password reset functionality needed
8. No pagination required (acceptable for demo scale)
9. Reviews are immediately published (no draft state)
10. Ratings are whole numbers (1, 2, 3, 4, 5 - no half stars)

---

## 7. Out of Scope (Future Enhancements)

- Comments on reviews
- Likes/upvotes
- User profiles
- Follow other users
- Email notifications
- Admin panel
- Content moderation
- Image uploads
- Integration with external APIs (TMDB, IGDB)
- Advanced search (full-text search)
- Pagination
- Password reset functionality
- Email verification
- Rate limiting
- Two-factor authentication

---

## 8. Risk Assessment

### High-Risk Items
1. **Security Vulnerabilities** - Implement all security measures from day one
2. **Data Loss** - Use Git from start, regular commits
3. **Browser Compatibility** - Test on multiple browsers throughout development

### Medium-Risk Items
1. **Performance Issues** - Monitor query performance, use indexes
2. **Usability Problems** - Test on actual mobile devices
3. **Scope Creep** - Stick to requirements, track feature requests separately

### Low-Risk Items
1. **Deployment Issues** - Document setup process clearly
2. **Dependency Updates** - Pin versions in requirements.txt

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-29 | Development Team | Initial requirements document |

---

## Approval

This requirements document serves as the foundation for the Movie & Game Review PWA project. All stakeholders should review and approve before development begins.

**Status:** Approved
**Date:** 2026-01-29
