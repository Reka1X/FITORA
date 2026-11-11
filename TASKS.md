# Fitora — Member Task Assignments

## Member 1 - Lwin Oo (Edward)
**Feature 1: Clothing Inventory**

**Goal:** Let users add and manage individual clothing items.

### Tasks
- Design the `clothing_items` SQLite table. Each item should store its name, photo, item type, style, selected color, selected item category, and availability.
- Implement `ClothingItem` and its subclasses `TopItem`, `BottomItem`, `OnePieceItem`, and `FootwearItem`.
- Demonstrate polymorphism through `outfit_role()`. The Shoes choice in the form must map to `FootwearItem`.
- Build Flask routes and pages to add, view, edit, and delete clothing items.
- Build the Add Clothing Item form so a user can:
  1. Take a photo or upload one.
  2. Enter the item name.
  3. Select a color from Member 2's catalog.
  4. Select an item type: Top, Bottom, Shoes, or One-piece.
  5. Select a style: Casual, Formal, or Street.
  6. Select an item category matching the selected type, for example, Jeans under Bottom.
  7. Submit the item.
- Include an "Add new category" option in the form. Send the category name and item type to Member 2's catalog feature, then make the new category available for selection. Users must not create colors from this form.
- Validate required fields, valid catalog selections, category/type matching, and category ownership. Reject a category belonging to another user.
- Accept JPG/PNG photos up to 5 MB.
- Provide a camera option that captures a photo for upload. Automatic clothing recognition is not required.
- Make new items available by default and allow users to change availability later.
- Add search and filters for item type, category, color, style, and availability.
- Provide item details and availability information to the Outfit Builder and Recommendation features. Members 3 and 5 are responsible for enforcing the rule that unavailable items cannot be included in new outfits or recommendations.
- Associate clothing items with the correct user account using `user_id`.
- Write at least 8 meaningful pytest tests covering creation, editing, deletion, missing fields, invalid categories, another user's category, uploads, filters, and availability.

### Files to Create

**Folder:** `features/clothing_inventory/`

```text
clothing_inventory/
├── __init__.py
├── models.py
├── routes.py
├── forms.py
├── services.py
└── templates/
    ├── clothing_list.html
    ├── clothing_detail.html
    ├── clothing_form.html
    └── partials/
        └── category_options.html
```

### File Responsibilities
- `__init__.py` — Initialize the Clothing Inventory Blueprint.
- `models.py` — Define `ClothingItem`, `TopItem`, `BottomItem`, `OnePieceItem`, and `FootwearItem`.
- `routes.py` — Implement add, view, edit, delete, search, and filter routes.
- `forms.py` — Define the clothing item form and validation rules.
- `services.py` — Handle image uploads, catalog selection validation, and communication with Member 2's catalog feature.
- `clothing_list.html` — Display clothing items with search and filters.
- `clothing_detail.html` — Display individual clothing item details and availability.
- `clothing_form.html` — Provide the Add/Edit Clothing Item form, including photo capture/upload and catalog selections.
- `partials/category_options.html` — Render category choices returned by the catalog feature, if a separate partial is needed.

### Deliverables
- Clothing inventory models, routes, forms, services, and templates.
- `clothing_items` database table.
- Camera capture and image upload functionality.
- Category and color selection integrated with Member 2's catalog.
- Feature tests and documentation in the shared `PROMPT_LOG.md`.

---

## Member 2 - Wathan Htat (Frost)
**Feature 2: Category & Color Catalog**

**Goal:** Manage the choices used by the Clothing Inventory form, including categories that users create for themselves.

### Tasks
- Design the `catalog_entries` SQLite table. A category should record its name, matching item type, and owner. Predefined categories and colors can be shared, while a user-created category belongs to that user.
- Implement `CatalogEntry`, `CategoryEntry`, and `ColorEntry`.
- Demonstrate polymorphism through `normalized_label()` and `describe_usage()`.
- Provide predefined colors and common categories, such as Black, Blue, T-shirt → Top, and Jeans → Bottom.
- Build a way for Member 1's form to retrieve available colors and categories.
- Return only categories matching the selected item type and visible to the current user.
- Build the category creation route used by Member 1's "Add new category" option.
- Save user-created categories under the current user's account.
- Build pages and routes for users to list, edit, and delete their own categories.
- Prevent users from changing another user's categories or shared predefined entries.
- Normalize names by removing extra whitespace and handling letter case.
- Prevent users from creating duplicate categories that are already available to them for the same item type.
- Validate the item type assigned to each category. For example, Jeans → Bottom is valid, while a clothing item marked Top cannot use the Jeans category.
- Prevent deletion of a category or color while clothing items still reference it.
- Display a clear message explaining why deletion was blocked.
- Add catalog search and filters by entry type and item type.
- Coordinate with Member 1 on how clothing items reference catalog entries, and with Member 4 on login and category ownership checks.
- Write at least 8 meaningful pytest tests covering creation, editing, deletion, normalization, duplicates, item type matching, ownership, visibility, and entries in use.

### Files to Create

**Folder:** `features/catalog/`

```text
catalog/
├── __init__.py
├── models.py
├── routes.py
├── forms.py
├── services.py
└── templates/
    ├── catalog_list.html
    ├── catalog_form.html
    └── partials/
        ├── color_options.html
        └── category_options.html
```

### File Responsibilities
- `__init__.py` — Initialize the Catalog Blueprint.
- `models.py` — Define `CatalogEntry`, `CategoryEntry`, and `ColorEntry`.
- `routes.py` — Implement catalog listing, category creation, editing, deletion, and catalog retrieval routes.
- `forms.py` — Define category and catalog forms with validation.
- `services.py` — Handle predefined catalog data, name normalization, duplicate checking, visibility, item type matching, and deletion restrictions.
- `catalog_list.html` — Display catalog entries with search and filters.
- `catalog_form.html` — Allow users to add or edit their own categories.
- `partials/color_options.html` — Provide available color choices for Member 1's clothing form.
- `partials/category_options.html` — Provide categories matching the selected item type and visible to the current user.

### Deliverables
- Catalog models, routes, forms, services, and templates.
- `catalog_entries` database table.
- Predefined catalog data for common colors and categories.
- Category and color interface usable by Member 1's clothing form.
- User-created category functionality with ownership restrictions.
- Feature tests and documentation in the shared `PROMPT_LOG.md`.

---

## Member 3 - Han Htoo Aung (Erics)
**Feature 3: Outfit Builder**

**Goal:** Allow users to combine clothing items and create their own outfits.

### Tasks
- Design the `outfits` and `outfit_items` SQLite tables.
- Implement `Outfit` and subclasses `CasualOutfit`, `FormalOutfit`, and `SportOutfit`.
- Demonstrate polymorphism through `compatibility_score(items)`.
- Build Flask routes to create, view, edit, and delete outfits.
- Create outfit forms and templates.
- Allow users to select clothing items from their own wardrobe.
- Require at least two distinct items in each outfit.
- Prevent duplicate items within an outfit.
- Exclude unavailable items from newly created outfits.
- Preserve item details in snapshots so saved outfits remain understandable if an item changes or is removed.
- Associate outfits with the correct user account using `user_id`.

### Files to Create

**Folder:** `features/outfit_builder/`

```text
outfit_builder/
├── __init__.py
├── models.py
├── routes.py
├── forms.py
└── templates/
    ├── outfit_list.html
    ├── outfit_detail.html
    └── outfit_form.html
```

### File Responsibilities
- `__init__.py` — Initialize the Outfit Builder Blueprint.
- `models.py` — Define the `Outfit` classes and outfit database operations.
- `routes.py` — Implement outfit creation, viewing, editing, and deletion routes.
- `forms.py` — Define outfit forms and clothing item selection.
- `outfit_list.html` — Display the user's saved outfits.
- `outfit_detail.html` — Display an outfit and its clothing items.
- `outfit_form.html` — Create and edit outfits.

### Deliverables
- Outfit models, routes, forms, and templates.
- `outfits` and `outfit_items` database tables.
- Outfit Builder functionality.
- Feature documentation in the shared `PROMPT_LOG.md`.

---

## Member 4 - Ngyein Chan Ko (Reka)
**Feature 4: User Account & Profile Management**

**Goal:** Handle user registration, authentication, and personal profile management.

### Tasks
- Design the `users` SQLite table.
- Implement a `User` base class and appropriate subclasses, such as `StandardUser` and `AdminUser` (only if administrator functionality is included).
- Demonstrate polymorphism through methods such as `get_profile_details()` and `get_permissions()`.
- Build Flask routes for account registration, login, logout, viewing profiles, and editing profiles.
- Create registration, login, and profile forms and templates.
- Allow users to create their own accounts.
- Validate registration information, including full name, email address, and password.
- Prevent duplicate accounts using email addresses.
- Implement secure password hashing; never store plain-text passwords.
- Implement session handling and authentication status.
- Allow users to view and edit personal profile information.
- Support optional profile picture uploads.
- Allow users to change their passwords securely.
- Restrict access to authenticated users where required.
- Ensure users can only view and manage their own profile information.
- Coordinate authentication integration with Member 7.

### Files to Create

**Folder:** `features/user_profile/`

```text
user_profile/
├── __init__.py
├── models.py
├── routes.py
├── forms.py
└── templates/
    ├── register.html
    ├── login.html
    ├── profile.html
    ├── edit_profile.html
    └── change_password.html
```

### File Responsibilities
- `__init__.py` — Initialize the User Profile Blueprint.
- `models.py` — Define the `User` class, subclasses, and user database operations.
- `routes.py` — Implement registration, login, logout, profile viewing, profile editing, and password changing routes.
- `forms.py` — Define registration, login, profile editing, and password change forms.
- `register.html` — Display the account registration form.
- `login.html` — Display the login form.
- `profile.html` — Display the user's personal profile.
- `edit_profile.html` — Allow users to edit their profile information.
- `change_password.html` — Allow users to securely change their password.

### Deliverables
- User account and profile models, routes, forms, and templates.
- `users` database table.
- Registration, login, logout, and profile management functionality.
- Feature documentation in the shared `PROMPT_LOG.md`.

**Important:** Member 4 owns the implementation of authentication. Member 7 only integrates the User Profile Blueprint into the main application. Do not implement registration and login separately in Member 7's files.

---

## Member 5 - Nyi Sett (August)
**Feature 5: Outfit Recommendations**

**Goal:** Generate outfit recommendations using the user's available clothing items.

### Tasks
- Design the `recommendations` and `recommendation_items` SQLite tables.
- Implement `Recommendation` and subclasses `ColorMatchRecommendation`, `OccasionMatchRecommendation`, and `CapsuleRecommendation`.
- Demonstrate polymorphism through `calculate_score()` and `explain_score()`.
- Build Flask routes to generate, view, and delete recommendations.
- Create recommendation result templates.
- Implement a documented rule-based scoring system that does not require a paid AI API.
- Require at least two distinct items in each recommendation.
- Exclude unavailable items.
- Check required clothing-role coverage based on the selected occasion and style preferences.
- Allow users to select occasion and style preferences when generating recommendations instead of using a separate style profile table.
- Display only recommendations scoring at least 60/100.
- Explain why each recommendation received its score.
- Preserve recommendation item details in snapshots.
- Associate recommendations with the correct user account using `user_id`.
- Coordinate data requirements with other feature owners.

### Files to Create

**Folder:** `features/recommendations/`

```text
recommendations/
├── __init__.py
├── models.py
├── routes.py
├── forms.py
├── engine.py
└── templates/
    ├── recommendation_list.html
    ├── recommendation_detail.html
    └── recommendation_form.html
```

### File Responsibilities
- `__init__.py` — Initialize the Recommendations Blueprint.
- `models.py` — Define the `Recommendation` classes and database operations.
- `routes.py` — Implement recommendation generation, viewing, and deletion routes.
- `forms.py` — Define occasion and style preference selection forms.
- `engine.py` — Implement recommendation algorithms, scoring, and explanation logic.
- `recommendation_list.html` — Display generated recommendations.
- `recommendation_detail.html` — Display recommendation details, scores, and explanations.
- `recommendation_form.html` — Allow users to select occasions and style preferences.

### Deliverables
- Recommendation models, routes, forms, and templates.
- Recommendation scoring and generation logic.
- `recommendations` and `recommendation_items` database tables.
- Feature documentation in the shared `PROMPT_LOG.md`.

**Important:** `CapsuleRecommendation` should suggest versatile clothing items that can create multiple outfit combinations. It should not simply recommend one outfit.

---

## Member 6 - Kaung Myat Tun (Kingston)
**Feature 6: Outfit Calendar & Wear History**

**Goal:** Allow users to schedule outfits and track their clothing history.

### Tasks
- Design the `outfit_schedules` and `wear_history` SQLite tables.
- Implement the `OutfitSchedule` base class and subclasses `CasualSchedule`, `WorkSchedule`, and `EventSchedule`.
- Demonstrate inheritance and polymorphism through schedule-specific descriptions or behavior.
- Build Flask routes to schedule, view, edit, and delete outfits.
- Create calendar, scheduling, and wear history templates.
- Allow users to select saved outfits from the Outfit Builder.
- Allow users to schedule outfits for specific dates.
- Display upcoming outfit schedules in a calendar or date-based view.
- Allow users to mark scheduled outfits as worn.
- Record and display previously worn outfits.
- Prevent duplicate scheduling of the same outfit on the same date.
- Allow users to view upcoming schedules and recently worn outfits.
- Use the existing `outfits` table from Member 3 instead of duplicating outfit information.
- Associate schedules and wear history with the correct user account using `user_id`.

### Files to Create

**Folder:** `features/outfit_calendar/`

```text
outfit_calendar/
├── __init__.py
├── models.py
├── routes.py
├── forms.py
└── templates/
    ├── calendar.html
    ├── schedule_outfit.html
    ├── schedule_detail.html
    └── wear_history.html
```

### File Responsibilities
- `__init__.py` — Initialize the Outfit Calendar Blueprint.
- `models.py` — Define the `OutfitSchedule` classes and wear history database operations.
- `routes.py` — Implement scheduling, calendar viewing, editing, deleting, and marking outfits as worn.
- `forms.py` — Define outfit scheduling forms.
- `calendar.html` — Display scheduled outfits in a calendar or date-based view.
- `schedule_outfit.html` — Allow users to schedule or edit an outfit.
- `schedule_detail.html` — Display individual schedule details.
- `wear_history.html` — Display previously worn outfits.

### Deliverables
- Outfit calendar models, routes, forms, and templates.
- `outfit_schedules` and `wear_history` database tables.
- Calendar and wear history functionality.
- Feature documentation in the shared `PROMPT_LOG.md`.

**Important:** Use the existing `outfits` table from Member 3 and reference its `outfit_id`. Do not create duplicate outfit records for calendar scheduling.

---

## Member 7 - Aung Khant Paing (Trevor)
**Core Application & Dashboard**

**Goal:** Develop the main Flask application structure and integrate all features into one working application.

### Tasks
- Set up and maintain the Flask application structure and configuration.
- Create and maintain the main application entry point using `app.py`.
- Configure application settings using `config.py`.
- Set up the shared SQLite database connection and initialization structure.
- Coordinate database initialization with all feature owners.
- Create the shared navigation, base layout, dashboard, and common error pages.
- Build reusable Bootstrap layouts and shared form/message components.
- Register and integrate all six feature blueprints.
- Integrate Member 4's registration, login, logout, and authentication functionality into the main application.
- Ensure users can navigate between all six features.
- Implement dashboard summaries using data from the feature modules, such as total clothing items, saved outfits, recommendations, upcoming schedules, and recently worn outfits.
- Configure shared static resources, CSS, JavaScript, and upload directories.
- Ensure user-level data access is correctly integrated across the application.
- Coordinate with all members to ensure their features work together in the main application.

### Files to Create

**Main Project Files**

```text
Fitora/
├── app.py
├── config.py
└── requirements.txt
```

**Core Folder**

```text
core/
├── __init__.py
├── db.py
├── base_model.py
└── helpers.py
```

**Dashboard Folder**

```text
dashboard/
├── __init__.py
└── routes.py
```

**Shared Templates**

```text
templates/
├── base.html
├── 404.html
├── 500.html
└── components/
    ├── navbar.html
    ├── flash_messages.html
    └── footer.html
```

**Static Resources**

```text
static/
├── css/
│   └── style.css
├── js/
│   └── main.js
└── images/
```

### File Responsibilities
- `app.py` — Create the Flask application and register all feature blueprints.
- `config.py` — Store application configuration, database settings, upload settings, and secret key configuration.
- `requirements.txt` — List the Python packages required by the project.
- `core/__init__.py` — Initialize shared core components.
- `core/db.py` — Manage SQLite database connections, shared initialization, and database configuration.
- `core/base_model.py` — Provide shared base model functionality if needed.
- `core/helpers.py` — Store reusable helper functions.
- `dashboard/__init__.py` — Initialize the Dashboard Blueprint.
- `dashboard/routes.py` — Implement dashboard routes and summary information.
- `base.html` — Provide the shared page layout.
- `404.html` — Display the page-not-found error.
- `500.html` — Display the internal-server-error page.
- `navbar.html` — Display shared navigation links.
- `flash_messages.html` — Display reusable success and error messages.
- `footer.html` — Provide the shared footer.
- `style.css` — Store shared application styles.
- `main.js` — Store shared JavaScript functionality.

### Deliverables
- Main Flask application setup and configuration.
- Shared database connection and initialization structure.
- Dashboard and shared templates.
- Blueprint registration and integration.
- Shared navigation and reusable components.

**Important:** Member 7 handles application integration and the dashboard. Member 4 owns the implementation of registration, login, logout, and profile management.

---

# Shared Project Requirements

## 1. Database Structure

Fitora uses SQLite to store application data.

| Table | Description |
|---|---|
| `users` | Stores user account credentials and personal profile information. |
| `clothing_items` | Stores clothing item information, catalog selections, photo, style, and availability. |
| `catalog_entries` | Stores predefined and user-created clothing categories and color definitions. |
| `outfits` | Stores outfit information. |
| `outfit_items` | Stores clothing item snapshots belonging to outfits. |
| `recommendations` | Stores recommendation information and scores. |
| `recommendation_items` | Stores clothing item snapshots included in recommendations. |
| `outfit_schedules` | Stores scheduled outfit references and their planned dates. |
| `wear_history` | Stores records of outfits marked as worn. |

## 2. Database Coordination

- Member 7 coordinates the shared database connection and initialization.
- Each feature member is responsible for designing and implementing the tables belonging to their feature.
- User-owned records must be associated with the correct `user_id`.
- Use foreign keys to connect related records.
- Enable SQLite foreign key enforcement.
- Use the existing `outfits` table for calendar scheduling and wear history instead of creating duplicate outfit records.
- The `catalog_entries` table provides shared category and color definitions.
- Member 1's `clothing_items` table should reference catalog entries using foreign keys, such as `color_id` and `category_id`.
- Member 2's catalog must distinguish shared predefined entries from user-created entries.
- Shared predefined catalog entries should not belong to an individual user.
- User-created categories must be associated with their creator's `user_id`.

## 3. Object-Oriented Programming Requirements

Each feature should demonstrate meaningful use of:

- Classes and objects.
- Encapsulation.
- Inheritance.
- Polymorphism.
- Appropriate methods and attributes.

Each member is responsible for implementing OOP concepts within their assigned feature.

## 4. Flask Architecture

- Use Flask for the backend.
- Use SQLite for data storage.
- Use HTML, CSS, and Bootstrap for the frontend.
- Organize each feature inside its own folder under `features/`.
- Use Flask Blueprints to separate feature routes.
- Use shared templates and reusable components where appropriate.

## 5. Shared Prompt Log

- Maintain only one `PROMPT_LOG.md` file at the project root.
- Each member must document their AI usage in their own section.
- Include prompts, AI-generated suggestions, how suggestions were applied, and any corrections made.
- Do not create separate prompt log files for individual features.

## 6. General Responsibilities

- Each member must implement their assigned feature.
- Follow the agreed project folder structure.
- Coordinate database relationships with relevant members.
- Use consistent naming conventions across the project.
- Ensure each feature integrates with the shared Flask application.
- Avoid duplicating functionality assigned to another member.
- Update shared documentation when changes affect the project structure or database design.