from core.db import get_db
from features.catalog.models import visible_categories


def normalize_label(label):
    return " ".join(label.split()).casefold()


def create_category(user_id, label, item_type):
    label = " ".join(label.split())

    if not label or item_type not in ("Top", "Bottom", "One-piece", "Shoes"):
        return False

    existing = visible_categories(user_id, item_type)
    label_key = normalize_label(label)

    if any(normalize_label(row["label"]) == label_key for row in existing):
        return False

    db = get_db()
    db.execute(
        """
        INSERT INTO catalog_entries (user_id, entry_type, label, item_type)
        VALUES (?, 'category', ?, ?)
        """,
        (user_id, label, item_type),
    )
    db.commit()
    return True


def update_category(user_id, entry_id, label, item_type):
    label = " ".join(label.split())

    if not label or item_type not in ("Top", "Bottom", "One-piece", "Shoes"):
        return False

    db = get_db()
    owned = db.execute(
        """
        SELECT id FROM catalog_entries
        WHERE id = ? AND user_id = ? AND entry_type = 'category'
        """,
        (entry_id, user_id),
    ).fetchone()

    if not owned:
        return False

    existing = visible_categories(user_id, item_type)
    label_key = normalize_label(label)

    for row in existing:
        if row["id"] != entry_id and normalize_label(row["label"]) == label_key:
            return False

    db.execute(
        """
        UPDATE catalog_entries
        SET label = ?, item_type = ?
        WHERE id = ? AND user_id = ? AND entry_type = 'category'
        """,
        (label, item_type, entry_id, user_id),
    )
    db.commit()
    return True


def delete_category(user_id, entry_id):
    db = get_db()

    owned = db.execute(
        """
        SELECT id FROM catalog_entries
        WHERE id = ? AND user_id = ? AND entry_type = 'category'
        """,
        (entry_id, user_id),
    ).fetchone()

    if not owned:
        return "not_owned"

    in_use = db.execute(
        "SELECT id FROM clothing_items WHERE category_id = ?",
        (entry_id,),
    ).fetchone()

    if in_use:
        return "in_use"

    db.execute(
        "DELETE FROM catalog_entries WHERE id = ? AND user_id = ?",
        (entry_id, user_id),
    )
    db.commit()
    return "deleted"