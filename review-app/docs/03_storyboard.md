# Storyboard & User Flows
## Movie & Game Review PWA

This document outlines user journeys and wireframe descriptions for key application flows.

---

## User Flow 1: New User Registration → First Review

### Narrative
Sarah wants to share her opinion about a game she just finished. She discovers the Review App but doesn't have an account yet.

### Flow Diagram
```
┌──────────────┐
│  Home Page   │ (Visitor sees all reviews)
└──────┬───────┘
       │ Clicks "Post Review" button
       ▼
┌──────────────┐
│Login Redirect│ (Not logged in, redirected to login)
└──────┬───────┘
       │ Clicks "Register" link
       ▼
┌──────────────────┐
│ Registration Page│
│                  │
│ [Username: ___]  │
│ [Email: ______]  │
│ [Password: ___]  │
│ [Confirm:  ___]  │
│                  │
│  [Register ▶]    │
└──────┬───────────┘
       │ Submits form with valid data
       ▼
┌──────────────┐
│Server Process│
│- Validate    │
│- Hash pass   │
│- Insert DB   │
└──────┬───────┘
       │ Success
       ▼
┌──────────────┐
│  Login Page  │ (Flash: "Registration successful!")
│              │
│ [Username:__]│
│ [Password:__]│
│              │
│  [Login ▶]   │
└──────┬───────┘
       │ Logs in with new credentials
       ▼
┌──────────────┐
│Server Process│
│- Verify hash │
│- Create sess │
└──────┬───────┘
       │ Success
       ▼
┌──────────────┐
│  Home Page   │ (Logged in - Flash: "Welcome, Sarah!")
│              │ (Nav shows: "My Reviews | Post Review | Logout")
└──────┬───────┘
       │ Clicks "Post Review"
       ▼
┌──────────────────┐
│Create Review Page│
│                  │
│ [Title: Hollow K]│
│ Category:        │
│  ○ Movie         │
│  ● Game          │
│ Rating: ★★★★★    │
│ [Review: ______] │
│                  │
│  [Post Review ▶] │
└──────┬───────────┘
       │ Submits review
       ▼
┌──────────────┐
│Server Process│
│- Validate    │
│- Sanitize    │
│- Insert DB   │
└──────┬───────┘
       │ Success
       ▼
┌──────────────┐
│  Home Page   │ (Flash: "Review posted!")
│              │ (Sarah's review appears at top)
└──────────────┘
```

### Wireframe Descriptions

#### Registration Page
```
┌────────────────────────────────────────┐
│ [Logo] Movie & Game Reviews            │
│ ────────────────────────────────────   │
│                                        │
│        Create Your Account             │
│                                        │
│  Username                              │
│  ┌──────────────────────────────────┐  │
│  │ john_doe                         │  │
│  └──────────────────────────────────┘  │
│  3-50 characters, letters & numbers    │
│                                        │
│  Email                                 │
│  ┌──────────────────────────────────┐  │
│  │ john@example.com                 │  │
│  └──────────────────────────────────┘  │
│                                        │
│  Password                              │
│  ┌──────────────────────────────────┐  │
│  │ ●●●●●●●●●●●●                     │  │
│  └──────────────────────────────────┘  │
│  Minimum 8 characters                  │
│  [Strength: ████████░░ Strong]         │
│                                        │
│  Confirm Password                      │
│  ┌──────────────────────────────────┐  │
│  │ ●●●●●●●●●●●●                     │  │
│  └──────────────────────────────────┘  │
│                                        │
│          ┌──────────────┐              │
│          │  Register ▶  │              │
│          └──────────────┘              │
│                                        │
│  Already have an account? Login        │
│                                        │
└────────────────────────────────────────┘
```

#### Create Review Page
```
┌────────────────────────────────────────┐
│ [Logo] Movie & Game Reviews            │
│ Home | My Reviews | Logout (Sarah)     │
│ ────────────────────────────────────   │
│                                        │
│        Post a New Review               │
│                                        │
│  Title (Movie or Game Name)            │
│  ┌──────────────────────────────────┐  │
│  │ Hollow Knight                    │  │
│  └──────────────────────────────────┘  │
│                                        │
│  Category                              │
│   ○ Movie    ● Game                    │
│                                        │
│  Your Rating                           │
│   ★ ★ ★ ★ ★  (clickable stars)         │
│   Currently: 5/5                       │
│                                        │
│  Your Review                           │
│  ┌──────────────────────────────────┐  │
│  │ An absolute masterpiece of       │  │
│  │ game design and storytelling.    │  │
│  │ The hand-drawn art style is      │  │
│  │ breathtaking, and the challenging│  │
│  │ gameplay keeps you engaged...    │  │
│  │                                  │  │
│  │                                  │  │
│  └──────────────────────────────────┘  │
│  Characters: 287/5000                  │
│  Minimum 10 characters                 │
│                                        │
│    ┌──────────────┐  ┌──────────────┐  │
│    │  Cancel      │  │ Post Review▶ │  │
│    └──────────────┘  └──────────────┘  │
│                                        │
└────────────────────────────────────────┘
```

---

## User Flow 2: Existing User → View → Edit Review

### Narrative
John has been using the app for a while. He wants to update a review he wrote last week after rewatching the movie.

### Flow Diagram
```
┌──────────────┐
│  Home Page   │ (John visits site)
└──────┬───────┘
       │ Clicks "Login"
       ▼
┌──────────────┐
│  Login Page  │
│              │
│ [Username:__]│
│ [Password:__]│
│  [Login ▶]   │
└──────┬───────┘
       │ Enters credentials
       ▼
┌──────────────┐
│Server Verify │
│- Check hash  │
│- Create sess │
└──────┬───────┘
       │ Success
       ▼
┌──────────────┐
│  Home Page   │ (Logged in)
│              │ (Sees all reviews including his own)
└──────┬───────┘
       │ Clicks "My Reviews" in nav
       ▼
┌──────────────────┐
│  My Reviews Page │
│                  │
│ Your Reviews (3) │
│                  │
│ ┌──────────────┐ │
│ │ The Matrix   │ │
│ │ ★★★★★ Posted │ │
│ │ "A groundbr" │ │
│ │ [Edit][Del]  │ │
│ └──────────────┘ │
│ ┌──────────────┐ │
│ │ Inception    │ │
│ │ ★★★★☆ Posted │ │
│ │ "Mind-bendi" │ │
│ │ [Edit][Del]  │ │◄─── Clicks Edit
│ └──────────────┘ │
│ ┌──────────────┐ │
│ │ Interstellar │ │
│ │ ★★★★★ Posted │ │
│ │ "Epic scienc"│ │
│ │ [Edit][Del]  │ │
│ └──────────────┘ │
│                  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│Server Check Auth │
│- Verify session  │
│- Check ownership │
│- Load review     │
└──────┬───────────┘
       │ Authorized
       ▼
┌──────────────────┐
│ Edit Review Page │
│                  │
│  Title           │
│  [Inception____] │
│                  │
│  Category        │
│   ● Movie ○ Game │
│                  │
│  Rating          │
│   ★★★★★          │◄─── Changes from 4 to 5 stars
│                  │
│  Review Text     │
│  [Mind-bending..] │◄─── Updates text
│  (pre-filled)    │
│                  │
│  [Cancel][Update]│
└──────┬───────────┘
       │ Clicks Update
       ▼
┌──────────────┐
│Server Process│
│- Verify auth │
│- Validate    │
│- Update DB   │
│- Set updated │
└──────┬───────┘
       │ Success
       ▼
┌──────────────┐
│ Review Detail│ (Flash: "Review updated!")
│              │ (Shows updated rating and text)
│              │ (Shows "Updated: Jan 29, 2026")
└──────────────┘
```

### Wireframe Descriptions

#### My Reviews Page
```
┌────────────────────────────────────────┐
│ [Logo] Movie & Game Reviews            │
│ Home | My Reviews | Logout (John)      │
│ ────────────────────────────────────   │
│                                        │
│   My Reviews (3 total)  [+Post New]    │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │ The Matrix               [MOVIE]   │ │
│ │ ★★★★★                    5/5       │ │
│ │ Posted: Jan 22, 2026               │ │
│ │ "A groundbreaking sci-fi film that │ │
│ │ explores reality and consciousness"│ │
│ │                                    │ │
│ │   [✏️ Edit]  [🗑️ Delete]            │ │
│ └────────────────────────────────────┘ │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │ Inception                [MOVIE]   │ │
│ │ ★★★★☆                    4/5       │ │
│ │ Posted: Jan 20, 2026               │ │
│ │ Updated: Jan 25, 2026              │ │
│ │ "Mind-bending thriller with layers"│ │
│ │                                    │ │
│ │   [✏️ Edit]  [🗑️ Delete]            │ │
│ └────────────────────────────────────┘ │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │ Interstellar             [MOVIE]   │ │
│ │ ★★★★★                    5/5       │ │
│ │ Posted: Jan 18, 2026               │ │
│ │ "Epic science fiction masterpiece" │ │
│ │                                    │ │
│ │   [✏️ Edit]  [🗑️ Delete]            │ │
│ └────────────────────────────────────┘ │
│                                        │
└────────────────────────────────────────┘
```

---

## User Flow 3: Guest User → Browse → Register Prompt

### Narrative
Emma is browsing the web and discovers the review app. She wants to read reviews before deciding to register.

### Flow Diagram
```
┌──────────────┐
│Search Engine │
│ (Google)     │
└──────┬───────┘
       │ Searches "Elden Ring reviews"
       │ Clicks link to Review App
       ▼
┌──────────────────┐
│   Home Page      │ (Guest User - Not Logged In)
│                  │
│ Nav: [Login] [Register]
│                  │
│ All Reviews (15) │
│                  │
│ Filters:         │
│ [All] [Movies]   │
│ [Games]          │
│                  │
│ ┌──────────────┐ │
│ │ Elden Ring   │ │
│ │ ★★★★★  5/5   │ │
│ │ by alex_wong │ │
│ │ "Masterpiece"│ │◄─── Emma clicks to read more
│ └──────────────┘ │
│ ┌──────────────┐ │
│ │ The Matrix   │ │
│ │ ★★★★★  5/5   │ │
│ └──────────────┘ │
│ ...more reviews  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Review Detail    │ (Can view full review as guest)
│                  │
│ Elden Ring [GAME]│
│ ★★★★★      5/5   │
│ by alex_wong     │
│ Posted: Jan 28   │
│                  │
│ (Full review txt)│
│ "An absolute ... │
│ masterpiece of...│
│ game design..."  │
│                  │
│ ┌──────────────┐ │
│ │ Want to post │ │
│ │ your own rev │ │
│ │ iew?         │ │
│ │              │ │
│ │ [Register]   │ │◄─── Emma decides to register
│ └──────────────┘ │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Registration Page│
│ (Same as Flow 1) │
└──────────────────┘
```

### Wireframe Descriptions

#### Home Page (Guest User)
```
┌────────────────────────────────────────┐
│ [Logo] Movie & Game Reviews            │
│              [Login]  [Register]       │
│ ────────────────────────────────────   │
│                                        │
│  Discover Reviews for Movies & Games   │
│                                        │
│  Filter by: [All ▾] [All Ratings ▾]    │
│                                        │
│  All Reviews (15)                      │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │ ┌──┐  Elden Ring         [GAME]   │ │
│ │ │  │  ★★★★★                        │ │
│ │ │  │  by alex_wong | Jan 28, 2026 │ │
│ │ └──┘  "An absolute masterpiece of  │ │
│ │       game design with incredible" │ │
│ │                                    │ │
│ │       [Read More →]                │ │
│ └────────────────────────────────────┘ │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │ ┌──┐  The Matrix        [MOVIE]   │ │
│ │ │  │  ★★★★★                        │ │
│ │ │  │  by john_doe | Jan 22, 2026  │ │
│ │ └──┘  "A groundbreaking sci-fi..."│ │
│ │                                    │ │
│ │       [Read More →]                │ │
│ └────────────────────────────────────┘ │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │ ┌──┐  Hollow Knight     [GAME]    │ │
│ │ │  │  ★★★★★                        │ │
│ │ │  │  by jane_smith | Jan 25      │ │
│ │ └──┘  "Beautiful Metroidvania..." │ │
│ │                                    │ │
│ │       [Read More →]                │ │
│ └────────────────────────────────────┘ │
│                                        │
│  ... more reviews ...                  │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │      Want to post your review?     │ │
│ │      [Register Free →]             │ │
│ └────────────────────────────────────┘ │
│                                        │
└────────────────────────────────────────┘
```

#### Review Detail Page (Guest View)
```
┌────────────────────────────────────────┐
│ [Logo] Movie & Game Reviews            │
│              [Login]  [Register]       │
│ ────────────────────────────────────   │
│                                        │
│  ← Back to All Reviews                 │
│                                        │
│  Elden Ring                   [GAME]   │
│  ★★★★★ (5/5)                           │
│                                        │
│  Reviewed by: alex_wong                │
│  Posted: January 28, 2026              │
│                                        │
│ ────────────────────────────────────   │
│                                        │
│  An absolute masterpiece of game       │
│  design with incredible world-building │
│  and challenging yet fair combat. The  │
│  exploration is rewarding, the bosses  │
│  are memorable, and the lore is deep   │
│  and mysterious. A must-play for any   │
│  fan of action RPGs. The difficulty is │
│  high but every victory feels earned.  │
│  Easily one of the best games of 2022. │
│                                        │
│ ────────────────────────────────────   │
│                                        │
│ ┌────────────────────────────────────┐ │
│ │   💭 Want to share your thoughts?  │ │
│ │                                    │ │
│ │   Create a free account to post    │ │
│ │   your own reviews!                │ │
│ │                                    │ │
│ │      [Register Now →]              │ │
│ │                                    │ │
│ │   Already have an account? [Login] │ │
│ └────────────────────────────────────┘ │
│                                        │
└────────────────────────────────────────┘
```

---

## User Flow 4: Delete Review with Confirmation

### Narrative
Jane wants to remove an old review she no longer agrees with.

### Flow Diagram
```
┌──────────────┐
│  My Reviews  │ (Jane's review list)
└──────┬───────┘
       │ Clicks "Delete" on a review
       ▼
┌──────────────────┐
│ JavaScript Popup │
│                  │
│ ⚠️ Are you sure? │
│                  │
│ This will perman │
│ -ently delete    │
│ your review.     │
│                  │
│ [Cancel][Delete] │◄─── Clicks Delete
└──────┬───────────┘
       │ Confirmed
       ▼
┌──────────────┐
│Server Process│
│- Verify auth │
│- Check owner │
│- DELETE query│
└──────┬───────┘
       │ Success
       ▼
┌──────────────┐
│  My Reviews  │ (Flash: "Review deleted")
│              │ (Review removed from list)
└──────────────┘
```

---

## User Flow 5: PWA Installation

### Narrative
Mike regularly uses the app on his phone and wants quick access.

### Flow Diagram
```
┌──────────────┐
│Mobile Browser│ (Chrome on Android)
└──────┬───────┘
       │ Visits app multiple times
       ▼
┌──────────────────┐
│ Browser detects  │
│ PWA criteria met │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Install Prompt  │
│                  │
│ "Add Movie &     │
│  Game Reviews to │
│  Home screen?"   │
│                  │
│ [Cancel][Install]│◄─── Mike clicks Install
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ App Installing   │
│ - Download icon  │
│ - Cache assets   │
│ - Register SW    │
└──────┬───────────┘
       │ Complete
       ▼
┌──────────────────┐
│  Home Screen     │
│                  │
│ [📱 Reviews App] │◄─── New icon appears
│                  │
│ Mike taps icon   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ App Opens in     │
│ Standalone Mode  │
│ (No browser UI)  │
│                  │
│ Full-screen exp  │
└──────────────────┘
```

---

## User Flow 6: Offline Access

### Narrative
Sarah is on a train with no internet but wants to read cached reviews.

### Flow Diagram
```
┌──────────────┐
│ User Online  │ (Visits app while connected)
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Service Worker   │
│ - Caches HTML    │
│ - Caches CSS     │
│ - Caches JS      │
│ - Caches images  │
└──────────────────┘
       │
       │ [Later...]
       ▼
┌──────────────┐
│ User Offline │ (Train loses signal)
│              │
│ Taps app icon│
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Service Worker   │
│ intercepts fetch │
│                  │
│ Serves from cache│
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  App Loads!      │
│                  │
│ [⚠️ Offline Mode]│
│                  │
│ (Cached reviews) │
│ (Read-only)      │
└──────────────────┘
```

---

## UI Element Specifications

### Navigation Bar
- **Logged Out:** Logo (left), Login (right), Register (right)
- **Logged In:** Logo (left), Home, My Reviews, Post Review, Logout, Username display

### Review Card (List View)
- Game/Movie title (h3)
- Category badge (pill shape, colored: blue for movie, green for game)
- Star rating (visual stars, not just number)
- Author username (link to future user profile)
- Date posted
- Review excerpt (150 characters with "...")
- "Read More" link

### Review Detail (Full View)
- Large title
- Category badge
- Full star rating
- Author name
- Posted date
- Updated date (if applicable, in smaller text)
- Full review text
- Edit/Delete buttons (only if user is owner)

### Forms
- Clear labels above inputs
- Input validation (red border on error)
- Error messages below field in red
- Success messages in green at top of form
- CSRF token (hidden field)
- Character count for text areas
- Password strength indicator

### Star Rating Input
- 5 clickable stars
- Hover effect (fills stars up to cursor)
- Click to set rating
- Currently selected rating shown below

### Buttons
- Primary action: Blue background, white text
- Secondary action: Gray outline, dark text
- Danger action (Delete): Red background, white text
- All buttons have hover state (slightly darker)

---

## Responsive Breakpoints

### Mobile (320px - 767px)
- Single column layout
- Full-width review cards
- Hamburger menu navigation
- Stacked form inputs
- Large touch-friendly buttons

### Tablet (768px - 1023px)
- Two-column review grid
- Side-by-side form inputs where appropriate
- Expanded navigation bar

### Desktop (1024px+)
- Three-column review grid
- Maximum content width: 1200px
- Centered layout with margins

---

## Accessibility Features

### Keyboard Navigation
- Tab order follows logical flow
- All interactive elements reachable via keyboard
- Focus indicators visible (blue outline)
- Skip to content link

### Screen Reader Support
- Semantic HTML (nav, main, article, aside)
- ARIA labels for icon buttons
- Alt text for all images
- Form labels associated with inputs

### Visual
- Color contrast ratio meets WCAG AA (4.5:1 for text)
- Text resizable up to 200%
- No information conveyed by color alone

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-29 | Development Team | Initial storyboard |
