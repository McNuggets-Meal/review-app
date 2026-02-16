# UML Diagrams
## Movie & Game Review PWA

This document contains UML Class Diagrams and Sequence Diagrams for the application architecture and key processes.

---

## 1. Class Diagram

### Complete System Class Diagram

```
┌───────────────────────────────────────┐
│            Flask App                  │
├───────────────────────────────────────┤
│ - secret_key: str                     │
│ - database_path: str                  │
├───────────────────────────────────────┤
│ + run(): void                         │
│ + register_blueprint(): void          │
│ + configure_security_headers(): void  │
└─────────────┬─────────────────────────┘
              │
              │ uses
              ▼
┌───────────────────────────────────────┐
│           User (Model)                │
├───────────────────────────────────────┤
│ - id: int                             │
│ - username: str                       │
│ - email: str                          │
│ - password_hash: str                  │
│ - created_at: datetime                │
├───────────────────────────────────────┤
│ + __init__(username, email, password) │
│ + create_user(): bool                 │
│ + get_by_username(username): User     │
│ + get_by_id(user_id): User           │
│ + get_by_email(email): User           │
│ + verify_password(password): bool     │
│ + to_dict(): dict                     │
└─────────────┬─────────────────────────┘
              │
              │ 1
              │
              │ has many
              │
              │ *
              ▼
┌───────────────────────────────────────┐
│         Review (Model)                │
├───────────────────────────────────────┤
│ - id: int                             │
│ - user_id: int (FK)                   │
│ - title: str                          │
│ - review_text: str                    │
│ - rating: int                         │
│ - review_date: datetime               │
│ - updated_at: datetime                │
│ - category: str                       │
├───────────────────────────────────────┤
│ + __init__(user_id, title, ...)      │
│ + create_review(): bool               │
│ + get_all_reviews(): List[Review]    │
│ + get_by_id(review_id): Review       │
│ + get_by_user_id(user_id): List      │
│ + update_review(): bool               │
│ + delete_review(): bool               │
│ + to_dict(): dict                     │
└───────────────────────────────────────┘


┌───────────────────────────────────────┐
│      SecurityUtils (Utility)          │
├───────────────────────────────────────┤
│ + hash_password(password): str        │
│ + verify_password(password, hash):bool│
│ + sanitize_input(text): str           │
└───────────────────────────────────────┘


┌───────────────────────────────────────┐
│      Validators (Utility)             │
├───────────────────────────────────────┤
│ + validate_username(username): bool   │
│ + validate_email(email): bool         │
│ + validate_password(password): bool   │
│ + validate_rating(rating): bool       │
│ + validate_review_text(text): bool    │
│ + validate_category(category): bool   │
└───────────────────────────────────────┘


┌───────────────────────────────────────┐
│    AuthMiddleware (Middleware)        │
├───────────────────────────────────────┤
│ + login_required(func): function      │
│ + check_ownership(func): function     │
└───────────────────────────────────────┘


┌───────────────────────────────────────┐
│     CSRFMiddleware (Middleware)       │
├───────────────────────────────────────┤
│ + generate_token(): str               │
│ + validate_token(token): bool         │
│ + csrf_protect(func): function        │
└───────────────────────────────────────┘


┌───────────────────────────────────────┐
│       AuthRoutes (Blueprint)          │
├───────────────────────────────────────┤
│ + register_get(): render_template     │
│ + register_post(): redirect           │
│ + login_get(): render_template        │
│ + login_post(): redirect              │
│ + logout(): redirect                  │
└───────────────────────────────────────┘


┌───────────────────────────────────────┐
│      ReviewRoutes (Blueprint)         │
├───────────────────────────────────────┤
│ + list_reviews(): render_template     │
│ + view_review(id): render_template    │
│ + create_review_get(): render         │
│ + create_review_post(): redirect      │
│ + edit_review_get(id): render         │
│ + edit_review_post(id): redirect      │
│ + delete_review(id): redirect         │
│ + my_reviews(): render_template       │
└───────────────────────────────────────┘
```

---

## 2. User Authentication Sequence Diagram

### User Registration Flow

```
┌──────┐    ┌──────────┐    ┌──────────┐    ┌────────────┐    ┌──────────┐
│Client│    │  Browser │    │ AuthRoute│    │Validators/ │    │ Database │
│      │    │          │    │          │    │ Security   │    │          │
└───┬──┘    └────┬─────┘    └────┬─────┘    └─────┬──────┘    └────┬─────┘
    │            │               │                 │                │
    │ 1. Fill    │               │                 │                │
    │ registration│              │                 │                │
    │ form       │               │                 │                │
    │────────────>               │                 │                │
    │            │               │                 │                │
    │        2. POST /register   │                 │                │
    │            │ (username,    │                 │                │
    │            │  email,       │                 │                │
    │            │  password,    │                 │                │
    │            │  csrf_token)  │                 │                │
    │            │──────────────>│                 │                │
    │            │               │                 │                │
    │            │               │ 3. Validate     │                │
    │            │               │    CSRF token   │                │
    │            │               │────────────────>│                │
    │            │               │                 │                │
    │            │               │ 4. Token valid  │                │
    │            │               │<────────────────│                │
    │            │               │                 │                │
    │            │               │ 5. Validate     │                │
    │            │               │    username     │                │
    │            │               │────────────────>│                │
    │            │               │                 │                │
    │            │               │ 6. Valid (3-50) │                │
    │            │               │<────────────────│                │
    │            │               │                 │                │
    │            │               │ 7. Validate     │                │
    │            │               │    email format │                │
    │            │               │────────────────>│                │
    │            │               │                 │                │
    │            │               │ 8. Valid email  │                │
    │            │               │<────────────────│                │
    │            │               │                 │                │
    │            │               │ 9. Check if     │                │
    │            │               │    username     │                │
    │            │               │    exists       │                │
    │            │               │─────────────────────────────────>│
    │            │               │                 │                │
    │            │               │ 10. Not found   │                │
    │            │               │    (available)  │                │
    │            │               │<─────────────────────────────────│
    │            │               │                 │                │
    │            │               │ 11. Hash        │                │
    │            │               │     password    │                │
    │            │               │     (bcrypt,    │                │
    │            │               │      12 rounds) │                │
    │            │               │────────────────>│                │
    │            │               │                 │                │
    │            │               │ 12. password_   │                │
    │            │               │     hash        │                │
    │            │               │<────────────────│                │
    │            │               │                 │                │
    │            │               │ 13. INSERT INTO │                │
    │            │               │     users       │                │
    │            │               │─────────────────────────────────>│
    │            │               │                 │                │
    │            │               │ 14. Success     │                │
    │            │               │     (user_id: 1)│                │
    │            │               │<─────────────────────────────────│
    │            │               │                 │                │
    │            │ 15. Redirect  │                 │                │
    │            │     to /login │                 │                │
    │            │     + flash   │                 │                │
    │            │<──────────────│                 │                │
    │            │               │                 │                │
    │ 16. Show   │               │                 │                │
    │ login page │               │                 │                │
    │<───────────│               │                 │                │
    │            │               │                 │                │
```

### User Login Flow

```
┌──────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│Client│    │  Browser │    │ AuthRoute│    │ Security │    │ Database │
└───┬──┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
    │            │               │                │                │
    │ 1. Enter   │               │                │                │
    │ credentials│               │                │                │
    │────────────>               │                │                │
    │            │               │                │                │
    │        2. POST /login      │                │                │
    │            │ (username,    │                │                │
    │            │  password,    │                │                │
    │            │  csrf_token)  │                │                │
    │            │──────────────>│                │                │
    │            │               │                │                │
    │            │               │ 3. Validate    │                │
    │            │               │    CSRF token  │                │
    │            │               │───────────────>│                │
    │            │               │                │                │
    │            │               │ 4. Token valid │                │
    │            │               │<───────────────│                │
    │            │               │                │                │
    │            │               │ 5. SELECT user │                │
    │            │               │    WHERE       │                │
    │            │               │    username=?  │                │
    │            │               │────────────────────────────────>│
    │            │               │                │                │
    │            │               │ 6. User record │                │
    │            │               │    (id, hash)  │                │
    │            │               │<────────────────────────────────│
    │            │               │                │                │
    │            │               │ 7. Verify      │                │
    │            │               │    password    │                │
    │            │               │    against hash│                │
    │            │               │───────────────>│                │
    │            │               │ bcrypt.check() │                │
    │            │               │ (constant-time)│                │
    │            │               │                │                │
    │            │               │ 8. Password    │                │
    │            │               │    matches     │                │
    │            │               │<───────────────│                │
    │            │               │                │                │
    │            │ 9. Create     │                │                │
    │            │    session    │                │                │
    │            │    session['  │                │                │
    │            │    user_id']  │                │                │
    │            │    =1         │                │                │
    │            │               │                │                │
    │            │ 10. Set cookie│                │                │
    │            │     HttpOnly  │                │                │
    │            │     SameSite  │                │                │
    │            │               │                │                │
    │            │ 11. Redirect  │                │                │
    │            │     to /      │                │                │
    │            │<──────────────│                │                │
    │            │               │                │                │
    │ 12. Home   │               │                │                │
    │ page       │               │                │                │
    │ (logged in)│               │                │                │
    │<───────────│               │                │                │
```

---

## 3. Create Review Sequence Diagram

```
┌──────┐  ┌────────┐  ┌──────────┐  ┌────────┐  ┌──────────┐  ┌────────┐
│Client│  │Browser │  │ReviewRoute│ │Middleware│ │Validators│  │Database│
└───┬──┘  └───┬────┘  └────┬─────┘  └────┬─────┘ └────┬─────┘  └───┬────┘
    │         │            │             │            │            │
    │ 1. Click "Post      │             │            │            │
    │    Review"          │             │            │            │
    │────────────>        │             │            │            │
    │         │           │             │            │            │
    │     2. GET /reviews/create        │            │            │
    │         │──────────>│             │            │            │
    │         │           │             │            │            │
    │         │           │ 3. Check    │            │            │
    │         │           │   @login_   │            │            │
    │         │           │    required │            │            │
    │         │           │────────────>│            │            │
    │         │           │             │            │            │
    │         │           │ 4. User in  │            │            │
    │         │           │    session  │            │            │
    │         │           │<────────────│            │            │
    │         │           │             │            │            │
    │         │ 5. Render form          │            │            │
    │         │    with CSRF            │            │            │
    │         │<──────────│             │            │            │
    │         │           │             │            │            │
    │ 6. Fill form        │             │            │            │
    │<────────│           │             │            │            │
    │         │           │             │            │            │
    │     7. POST /reviews/create       │            │            │
    │         │ (title, rating,         │            │            │
    │         │  review_text,           │            │            │
    │         │  category,              │            │            │
    │         │  csrf_token)            │            │            │
    │         │──────────>│             │            │            │
    │         │           │             │            │            │
    │         │           │ 8. Verify   │            │            │
    │         │           │    CSRF     │            │            │
    │         │           │────────────>│            │            │
    │         │           │             │            │            │
    │         │           │ 9. Valid    │            │            │
    │         │           │<────────────│            │            │
    │         │           │             │            │            │
    │         │           │ 10. Validate│            │            │
    │         │           │     inputs  │            │            │
    │         │           │─────────────────────────>│            │
    │         │           │             │ title: OK  │            │
    │         │           │             │ rating: OK │            │
    │         │           │             │ text: OK   │            │
    │         │           │             │ category:OK│            │
    │         │           │ 11. All     │            │            │
    │         │           │     valid   │            │            │
    │         │           │<─────────────────────────│            │
    │         │           │             │            │            │
    │         │           │ 12. Sanitize│            │            │
    │         │           │     inputs  │            │            │
    │         │           │     (XSS)   │            │            │
    │         │           │─────────────────────────>│            │
    │         │           │             │            │            │
    │         │           │ 13. Clean   │            │            │
    │         │           │     data    │            │            │
    │         │           │<─────────────────────────│            │
    │         │           │             │            │            │
    │         │           │ 14. INSERT INTO reviews  │            │
    │         │           │     (user_id=session,    │            │
    │         │           │      title, ...)         │            │
    │         │           │──────────────────────────────────────>│
    │         │           │             │            │            │
    │         │           │ 15. Success (review_id)  │            │
    │         │           │<──────────────────────────────────────│
    │         │           │             │            │            │
    │         │ 16. Redirect            │            │            │
    │         │     to /                │            │            │
    │         │     + flash             │            │            │
    │         │<──────────│             │            │            │
    │         │           │             │            │            │
    │ 17. Home│           │             │            │            │
    │ with new│           │             │            │            │
    │ review  │           │             │            │            │
    │<────────│           │             │            │            │
```

---

## 4. Edit Review with Authorization Sequence Diagram

```
┌──────┐  ┌────────┐  ┌──────────┐  ┌────────┐  ┌────────┐
│Client│  │Browser │  │ReviewRoute│ │Middleware│ │Database│
└───┬──┘  └───┬────┘  └────┬─────┘  └────┬─────┘ └───┬────┘
    │         │            │             │            │
    │ 1. Click "Edit"     │             │            │
    │    on review        │             │            │
    │────────────>        │             │            │
    │         │           │             │            │
    │     2. GET /reviews/5/edit        │            │
    │         │──────────>│             │            │
    │         │           │             │            │
    │         │           │ 3. Check    │            │
    │         │           │   @login_   │            │
    │         │           │    required │            │
    │         │           │────────────>│            │
    │         │           │             │            │
    │         │           │ 4. User     │            │
    │         │           │    logged in│            │
    │         │           │<────────────│            │
    │         │           │             │            │
    │         │           │ 5. SELECT review        │
    │         │           │    WHERE id=5           │
    │         │           │─────────────────────────>│
    │         │           │             │            │
    │         │           │ 6. Review   │            │
    │         │           │    (user_id=1)          │
    │         │           │<─────────────────────────│
    │         │           │             │            │
    │         │           │ 7. Check    │            │
    │         │           │    ownership│            │
    │         │           │    session['│            │
    │         │           │    user_id']│            │
    │         │           │    == review│            │
    │         │           │    .user_id │            │
    │         │           │             │            │
    │         │     ┌─────┴──────┐      │            │
    │         │     │IF user_id  │      │            │
    │         │     │matches:    │      │            │
    │         │     │  Allow     │      │            │
    │         │     │ELSE:       │      │            │
    │         │     │  403 Error │      │            │
    │         │     └─────┬──────┘      │            │
    │         │           │             │            │
    │         │ 8. Render│             │            │
    │         │    edit form            │            │
    │         │    pre-filled           │            │
    │         │<──────────│             │            │
    │         │           │             │            │
    │ 9. Modify           │             │            │
    │    fields           │             │            │
    │<────────│           │             │            │
    │         │           │             │            │
    │     10. POST /reviews/5/edit      │            │
    │         │ (updated data)          │            │
    │         │──────────>│             │            │
    │         │           │             │            │
    │         │           │ 11. Verify  │            │
    │         │           │     owner   │            │
    │         │           │     again   │            │
    │         │           │─────────────────────────>│
    │         │           │             │            │
    │         │           │ 12. Owner   │            │
    │         │           │     confirmed            │
    │         │           │<─────────────────────────│
    │         │           │             │            │
    │         │           │ 13. UPDATE reviews      │
    │         │           │     SET title=?,        │
    │         │           │     updated_at=NOW()    │
    │         │           │     WHERE id=5          │
    │         │           │─────────────────────────>│
    │         │           │             │            │
    │         │           │ 14. Success │            │
    │         │           │<─────────────────────────│
    │         │           │             │            │
    │         │ 15. Redirect            │            │
    │         │<──────────│             │            │
    │         │           │             │            │
    │ 16. View│           │             │            │
    │ updated │           │             │            │
    │<────────│           │             │            │
```

---

## 5. Service Worker (PWA) Activity Diagram

```
                    ┌─────────────────┐
                    │  Browser loads  │
                    │  application    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Register Service│
                    │    Worker       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  SW Install     │
                    │  Event Fires    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Cache Static    │
                    │ Resources:      │
                    │ - CSS files     │
                    │ - JS files      │
                    │ - Images        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ SW Activate     │
                    │ Event Fires     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Clean Old Caches│
                    └────────┬────────┘
                             │
                   ┌─────────▼─────────┐
                   │                   │
                   │  SW Ready & Active│
                   │                   │
                   └─────────┬─────────┘
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
   ┌────────────────┐              ┌────────────────┐
   │ Fetch Event    │              │  User Goes     │
   │ (Network       │              │  Offline       │
   │  Request)      │              │                │
   └────────┬───────┘              └────────┬───────┘
            │                               │
            ▼                               ▼
   ┌────────────────┐              ┌────────────────┐
   │ Check Cache    │              │ Fetch Event    │
   │ for Resource   │              │ Fires          │
   └────────┬───────┘              └────────┬───────┘
            │                               │
       ┌────▼────┐                          │
       │ Found?  │                          │
       └────┬────┘                          │
            │                               │
    ┌───────┴───────┐                       │
    │               │                       │
    ▼               ▼                       ▼
┌────────┐     ┌──────────┐        ┌───────────────┐
│ Yes    │     │  No      │        │ Check Cache   │
│ Serve  │     │ Fetch    │        │               │
│ from   │     │ from     │        └───────┬───────┘
│ Cache  │     │ Network  │                │
│        │     │          │            ┌───▼───┐
└────────┘     └────┬─────┘            │Found? │
                    │                  └───┬───┘
                    ▼                      │
           ┌────────────────┐         ┌───┴───┐
           │ Optionally     │         │       │
           │ Cache Response │         ▼       ▼
           └────────────────┘     ┌──────┐ ┌──────┐
                                  │ Yes  │ │  No  │
                                  │Serve │ │ Show │
                                  │Cache │ │Error │
                                  └──────┘ └──────┘
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-29 | Development Team | Initial UML diagrams |
