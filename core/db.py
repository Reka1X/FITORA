import sqlite3

from flask import current_app, g


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    profile_picture TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS catalog_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    entry_type TEXT NOT NULL CHECK (entry_type IN ('color', 'category')),
    label TEXT NOT NULL,
    item_type TEXT
);

CREATE TABLE IF NOT EXISTS clothing_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    photo TEXT,
    item_type TEXT NOT NULL,
    style TEXT NOT NULL,
    color_id INTEGER REFERENCES catalog_entries(id),
    category_id INTEGER REFERENCES catalog_entries(id),
    available INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS outfits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    outfit_type TEXT NOT NULL,
    description TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS outfit_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    outfit_id INTEGER NOT NULL REFERENCES outfits(id) ON DELETE CASCADE,
    clothing_item_id INTEGER,
    item_name TEXT NOT NULL,
    item_type TEXT NOT NULL,
    style TEXT NOT NULL,
    color TEXT,
    category TEXT
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    recommendation_type TEXT NOT NULL,
    occasion TEXT NOT NULL,
    style TEXT NOT NULL,
    score INTEGER NOT NULL,
    explanation TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendation_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_id INTEGER NOT NULL REFERENCES recommendations(id) ON DELETE CASCADE,
    item_name TEXT NOT NULL,
    item_type TEXT NOT NULL,
    style TEXT NOT NULL,
    color TEXT,
    category TEXT
);

CREATE TABLE IF NOT EXISTS outfit_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    outfit_id INTEGER NOT NULL REFERENCES outfits(id) ON DELETE CASCADE,
    planned_date TEXT NOT NULL,
    schedule_type TEXT NOT NULL DEFAULT 'Casual',
    note TEXT DEFAULT '',
    UNIQUE (user_id, outfit_id, planned_date)
);

CREATE TABLE IF NOT EXISTS wear_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    outfit_id INTEGER NOT NULL REFERENCES outfits(id) ON DELETE CASCADE,
    worn_date TEXT NOT NULL,
    UNIQUE (user_id, outfit_id, worn_date)
);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db():
    db = get_db()
    db.executescript(SCHEMA)

    # Migrate databases created before schedule_type was added.
    columns = {
        row["name"]
        for row in db.execute("PRAGMA table_info(outfit_schedules)").fetchall()
    }
    if "schedule_type" not in columns:
        db.execute(
            """
            ALTER TABLE outfit_schedules
            ADD COLUMN schedule_type TEXT NOT NULL DEFAULT 'Casual'
            """
        )

    colors = ["Black", "White", "Blue", "Red", "Green", "Beige", "Brown", "Grey"]
    categories = [
        ("T-shirt", "Top"),
        ("Shirt", "Top"),
        ("Sweater", "Top"),
        ("Jeans", "Bottom"),
        ("Trousers", "Bottom"),
        ("Skirt", "Bottom"),
        ("Dress", "One-piece"),
        ("Jumpsuit", "One-piece"),
        ("Sneakers", "Shoes"),
    ]

    for label in colors:
        db.execute(
            """
            INSERT INTO catalog_entries (entry_type, label)
            SELECT 'color', ?
            WHERE NOT EXISTS (
                SELECT 1 FROM catalog_entries
                WHERE entry_type = 'color' AND label = ? AND user_id IS NULL
            )
            """,
            (label, label),
        )

    for label, item_type in categories:
        db.execute(
            """
            INSERT INTO catalog_entries (entry_type, label, item_type)
            SELECT 'category', ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM catalog_entries
                WHERE entry_type = 'category'
                  AND label = ?
                  AND item_type = ?
                  AND user_id IS NULL
            )
            """,
            (label, item_type, label, item_type),
        )

    db.commit()
