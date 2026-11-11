# Fitora

> A Flask and SQLite digital wardrobe and outfit assistant that helps users manage accounts, organize clothing, build outfits, plan what to wear, and receive explainable outfit recommendations.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

## 1. Project Overview

Fitora is a web-based digital wardrobe and outfit-planning application developed using Python, Flask, and SQLite.

The application allows users to create accounts and manage personal profiles, organize clothing collections, manage clothing categories and colors, build outfits, receive personalized outfit recommendations, and schedule outfits using a calendar with wear-history tracking.

The project is developed by a seven-member team for **192-201 Advanced Computer Programming with Generative AI**.

The core recommendation system uses deterministic, rule-based scoring so that recommendations are consistent and explainable. Users select occasion and style preferences when requesting recommendations. A separate saved style-profile feature is not included in the current project scope.

Generative AI may optionally be used to generate natural-language explanations, but it is not required for the application to function.

## 2. Main Features

Fitora consists of six independent features and a shared core application.

| Feature | Description | Database Tables | Developer |
|---|---|---|---|
| Clothing Inventory | Add, view, edit, delete, search, and filter wardrobe items, including photos and availability. | `clothing_items` | Member 1 |
| Category & Color Catalog | Manage predefined colors and categories, plus user-created categories. | `catalog_entries` | Member 2 |
| Outfit Builder | Create, view, edit, and delete outfits using available clothing items. | `outfits`, `outfit_items` | Member 3 |
| User Account & Profile Management | Register, log in, log out, and manage personal profile information. | `users` | Member 4 |
| Outfit Recommendations | Generate and explain outfit recommendations using rule-based scoring. | `recommendations`, `recommendation_items` | Member 5 |
| Outfit Calendar & Wear History | Schedule saved outfits for specific dates, mark outfits as worn, and view previous wear records. | `outfit_schedules`, `wear_history` | Member 6 |

### Key Capabilities

- Register, log in, and manage personal accounts.
- Add, update, and manage wardrobe items.
- Take clothing photos or upload images.
- Organize clothing by category, color, item type, and style.
- Create personal clothing categories.
- Search and filter clothing collections.
- Create and manage different outfit combinations.
- Select occasion and style preferences when generating recommendations.
- Generate outfit recommendations with explainable scores.
- Schedule saved outfits for specific dates.
- View upcoming outfit schedules in a calendar or date-based view.
- Mark scheduled outfits as worn and review wear history.
- Validate user input and display appropriate feedback.
- Store application data using SQLite.

## 3. Team Members

| No. | Name | Student ID | GitHub |
|---|---|---|---|
| 1 | Lwin Oo | 6705140051 | [lwinDoubleOmega](https://github.com/lwinDoubleOmega) |
| 2 | Wathan Htat | 6705140052 | [callmefrost27-dotcom](https://github.com/callmefrost27-dotcom) |
| 3 | Han Htoo Aung | 6705140067 | [Erics12487254](https://github.com/Erics12487254) |
| 4 | Ngyein Chan Ko | 6705140061 | [Reka1X](https://github.com/Reka1X) |
| 5 | Nyi Sett | 6705140078 | [Whale_0134](https://github.com/Whale_0134) |
| 6 | Kaung Myat Tun | 6705140059 | [Kaungmyattun8](https://github.com/Kaungmyattun8) |
| 7 | Aung Khant Paing | 6705140082 | [Trevor0v0](https://github.com/Trevor0v0) |

**Group Number:** To be confirmed

**Team Leader:** Lwin Oo

### Member Responsibilities

| Member | Responsibility |
|---|---|
| Member 1 | Clothing Inventory |
| Member 2 | Category & Color Catalog |
| Member 3 | Outfit Builder |
| Member 4 | User Account & Profile Management |
| Member 5 | Outfit Recommendations |
| Member 6 | Outfit Calendar & Wear History |
| Member 7 | Core Application & Dashboard |

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Backend web framework |
| SQLite | Database management |
| HTML | Web page structure |
| CSS | Styling |
| Bootstrap | Responsive user interface |
| Jinja | Dynamic HTML templates |
| Git & GitHub | Version control and collaboration |

## 5. Project Architecture

The application follows a modular Flask architecture. Each feature is implemented using an independent Flask Blueprint.

Each feature maintains its own models, routes, forms or engine, and templates.

Member 4 implements account registration, login, logout, session handling, and profile management inside the User Account & Profile Management feature.

Member 7 maintains the shared application structure, database connection, navigation, and dashboard, and registers Member 4's Blueprint.

The project uses one shared `PROMPT_LOG.md` at the repository root. The responsibilities for all seven members are defined in [`TASKS.md`](TASKS.md).

```text
                         User / Browser
                              |
                              v
                       Flask Application
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
   User Account &      Clothing Inventory   Category & Color
 Profile Management                         Catalog
          |                   |                   |
          +-------------------+-------------------+
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
    Outfit Builder      Recommendations     Outfit Calendar
                                              & Wear History
                              |
                              v
                       SQLite Database
```

Feature modules should remain modular and communicate through clearly defined functions or shared data models.

For example:
- Clothing Inventory retrieves categories and colors from the Category & Color Catalog.
- Outfit Builder uses available clothing items from Clothing Inventory.
- Outfit Recommendations use wardrobe data and selected occasion/style preferences.
- Outfit Calendar references saved outfits through the existing `outfits` table rather than duplicating outfit records.
- The Dashboard retrieves summary information from the different features.

## 6. Getting Started

### Prerequisites

Before running the project, make sure you have installed:

- Python 3.10 or later
- Git
- Visual Studio Code or another code editor

### Step 1: Clone the Repository

```bash
git clone https://github.com/lwinDoubleOmega/ACP_final_project_edamame
```

Navigate into the project directory:

```bash
cd Fitora
```

### Step 2: Create a Virtual Environment

For Windows PowerShell:

```powershell
py -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

For macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The project's dependencies should be maintained in `requirements.txt`. At minimum, Flask is expected.

### Step 4: Run the Application

Follow the database initialization and configuration instructions provided by the actual project starter code.

If the application entry point is `app.py`, run:

```bash
python app.py
```

Alternatively, if Flask CLI is configured:

```bash
flask --app app run --debug
```

Open the local address shown in your terminal, usually:

```text
http://127.0.0.1:5000/
```

## 7. Database Structure

Fitora uses SQLite to store application data.

| Table | Description |
|---|---|
| `users` | Stores user account credentials and personal profile information. |
| `clothing_items` | Stores clothing item information, catalog references, photos, style, and availability. |
| `catalog_entries` | Stores predefined and user-created clothing categories and color definitions. |
| `outfits` | Stores outfit information. |
| `outfit_items` | Stores clothing item snapshots belonging to outfits. |
| `recommendations` | Stores recommendation information and scores. |
| `recommendation_items` | Stores clothing item snapshots included in recommendations. |
| `outfit_schedules` | Stores scheduled outfit references and their planned dates. |
| `wear_history` | Stores records of outfits marked as worn. |

All database operations must use parameterized SQL queries to prevent SQL injection.

### Database Relationships and Rules

- The `clothing_items` table should reference catalog entries using IDs such as `color_id` and `category_id`, rather than storing catalog names as plain text.
- User-created categories must be associated with their owner through `user_id`.
- Shared predefined catalog entries may have no individual owner.
- User-owned records across the application should be scoped by `user_id`.
- SQLite foreign-key enforcement must be enabled.
- Outfit and recommendation records use item snapshots so that previously saved results do not unexpectedly change when an inventory item is edited.
- The calendar feature should reference existing `outfits` records using their IDs and should not create duplicate outfit records.
- Categories and colors cannot be deleted while clothing items still reference them.

## 8. Object-Oriented Programming

Inheritance and polymorphism are important requirements of this project.

Each feature implements its own meaningful class hierarchy with overridden methods.

| Feature | Parent Class | Child Classes | Polymorphic Methods |
|---|---|---|---|
| Clothing Inventory | `ClothingItem` | `TopItem`, `BottomItem`, `OnePieceItem`, `FootwearItem` | `outfit_role()` |
| Category & Color Catalog | `CatalogEntry` | `CategoryEntry`, `ColorEntry` | `normalized_label()`, `describe_usage()` |
| Outfit Builder | `Outfit` | `CasualOutfit`, `FormalOutfit`, `SportOutfit` | `compatibility_score(items)` |
| User Account & Profile Management | `User` | `StandardUser`, optional `AdminUser` | `get_profile_details()`, `get_permissions()` |
| Outfit Recommendations | `Recommendation` | `ColorMatchRecommendation`, `OccasionMatchRecommendation`, `CapsuleRecommendation` | `calculate_score()`, `explain_score()` |
| Outfit Calendar & Wear History | `OutfitSchedule` | `CasualSchedule`, `WorkSchedule`, `EventSchedule` | Schedule-specific descriptions or behavior |

Feature entities should inherit from the lecturer-provided `BaseModel` where required.

Each model should demonstrate:

- Encapsulation using validated properties.
- Inheritance from appropriate parent classes.
- Polymorphism through overridden methods.
- Readable `__str__()` methods.
- Appropriate data operations such as `save()`, `find_all()`, `update()`, and `delete()`.

## 9. Project Structure

The agreed project structure is:

```text
Fitora/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── PROJECT_SCOPE.md
├── TASKS.md
├── PROMPT_LOG.md
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── db.py
│   ├── base_model.py
│   └── helpers.py
│
├── dashboard/
│   ├── __init__.py
│   └── routes.py
│
├── templates/
│   ├── base.html
│   ├── 404.html
│   ├── 500.html
│   └── components/
│       ├── navbar.html
│       ├── flash_messages.html
│       └── footer.html
│
├── features/
│   ├── __init__.py
│   │
│   ├── clothing_inventory/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   ├── services.py
│   │   └── templates/
│   │       ├── clothing_list.html
│   │       ├── clothing_detail.html
│   │       ├── clothing_form.html
│   │       └── partials/
│   │           └── category_options.html
│   │
│   ├── catalog/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   ├── services.py
│   │   └── templates/
│   │       ├── catalog_list.html
│   │       ├── catalog_form.html
│   │       └── partials/
│   │           ├── color_options.html
│   │           └── category_options.html
│   │
│   ├── outfit_builder/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/
│   │       ├── outfit_list.html
│   │       ├── outfit_detail.html
│   │       └── outfit_form.html
│   │
│   ├── user_profile/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/
│   │       ├── register.html
│   │       ├── login.html
│   │       ├── profile.html
│   │       ├── edit_profile.html
│   │       └── change_password.html
│   │
│   ├── recommendations/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   ├── engine.py
│   │   └── templates/
│   │       ├── recommendation_list.html
│   │       ├── recommendation_detail.html
│   │       └── recommendation_form.html
│   │
│   └── outfit_calendar/
│       ├── __init__.py
│       ├── models.py
│       ├── routes.py
│       ├── forms.py
│       └── templates/
│           ├── calendar.html
│           ├── schedule_outfit.html
│           ├── schedule_detail.html
│           └── wear_history.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
├── uploads/
│
└── instance/
```

The final structure should follow the lecturer's starter repository and the team's agreed implementation.

Authentication is implemented inside `features/user_profile/` by Member 4. Member 7 registers that Blueprint in the main application and does not duplicate its routes or logic.

## 10. Project Scope

### Included in the Minimum Viable Product

- User registration, login, logout, session handling, and profile management.
- CRUD functionality for wardrobe items, user-created categories, outfits, recommendations, and schedules where applicable.
- Clothing photo upload and camera capture (JPG/PNG, up to 5 MB).
- Search and filtering where applicable.
- Input validation and appropriate user feedback.
- Feature-specific business rules and user-level data ownership.
- SQLite database integration and predefined catalog data.
- Responsive browser interface.
- Meaningful inheritance and polymorphism.
- Rule-based outfit recommendations with explainable scores.
- Outfit scheduling and wear-history records.
- Shared navigation and dashboard functionality.

### Outside the Minimum Viable Product

- Administrator-level account management beyond the agreed user account and profile functionality.
- Online shopping and payment systems.
- Required paid or hosted AI APIs.
- Automatic body measurements or body-shape inference.
- Automatic AI-based clothing recognition or classification. Users may take or upload clothing photos, but the application does not automatically identify clothing.
- Mobile applications.
- Cloud synchronization and production hosting.

## 11. Generative AI Usage

Generative AI tools may be used to support:

- Project brainstorming and planning.
- Understanding object-oriented programming concepts.
- Drafting repetitive application code.
- Reviewing validation logic.
- Explaining programming errors.
- Improving documentation.

All AI-generated code must be reviewed, understood, and modified when necessary by the team.

The team maintains one shared `PROMPT_LOG.md` at the repository root. Add an entry for each AI-assisted contribution, identifying the member and task so the record remains attributable.

The prompt log should include:

1. Prompts given to AI tools.
2. AI-generated suggestions or code used.
3. Modifications made by the developer.
4. How the final contribution was reviewed and verified.

Only fake or sample data should be used with AI tools. No real personal or institutional data should be shared.

Every team member must be able to explain their own implementation during the project defence.

## 12. Contribution Guidelines

To maintain a clean and organized development workflow:

1. Work mainly inside your assigned feature folder.
2. Discuss shared-file changes with the team before editing.
3. Create a separate Git branch for your feature.
4. Verify that your changes work with the related feature functionality.
5. Use meaningful commit messages.
6. Review changes before merging into the main branch.

Example Git workflow:

```bash
git checkout -b feature/your-feature-name
```

Add and commit your changes:

```bash
git add .
git commit -m "Add clothing inventory functionality"
```

Push your branch:

```bash
git push -u origin feature/your-feature-name
```

Do not modify lecturer-provided shared files such as `app.py`, `core/db.py`, `core/base_model.py`, or `templates/base.html` unless the lecturer authorizes it or the team has agreed on the change.

## 13. Project Information

| Item | Details |
|---|---|
| Project Name | Fitora |
| Course | 192-201 Advanced Computer Programming with Generative AI |
| Project Type | Term Project |
| Team Size | 7 Members |
| Backend | Flask |
| Database | SQLite |
| Group Number | To be confirmed |
| Team Leader | Lwin Oo |
| GitHub Repository | https://github.com/lwinDoubleOmega/ACP_final_project_edamame |

---

**Fitora — Organize your wardrobe. Build your style.**