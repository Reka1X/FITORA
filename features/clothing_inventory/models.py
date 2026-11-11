from core.db import get_db


class ClothingItem:
    role = "item"

    def __init__(self, row):
        self.row = row

    def outfit_role(self):
        return self.role


class TopItem(ClothingItem):
    role = "top"


class BottomItem(ClothingItem):
    role = "bottom"


class OnePieceItem(ClothingItem):
    role = "one-piece"


class FootwearItem(ClothingItem):
    role = "shoes"


ITEM_CLASSES = {
    "Top": TopItem,
    "Bottom": BottomItem,
    "One-piece": OnePieceItem,
    "Shoes": FootwearItem,
}


def get_item(user_id, item_id):
    return get_db().execute(
        """
        SELECT
            clothing_items.*,
            colors.label AS color,
            categories.label AS category
        FROM clothing_items
        LEFT JOIN catalog_entries AS colors
            ON colors.id = clothing_items.color_id
        LEFT JOIN catalog_entries AS categories
            ON categories.id = clothing_items.category_id
        WHERE clothing_items.user_id = ?
          AND clothing_items.id = ?
        """,
        (user_id, item_id),
    ).fetchone()


def list_items(user_id, filters=None):
    filters = filters or {}

    sql = """
        SELECT
            clothing_items.*,
            colors.label AS color,
            categories.label AS category
        FROM clothing_items
        LEFT JOIN catalog_entries AS colors
            ON colors.id = clothing_items.color_id
        LEFT JOIN catalog_entries AS categories
            ON categories.id = clothing_items.category_id
        WHERE clothing_items.user_id = ?
    """
    args = [user_id]

    if filters.get("q"):
        sql += " AND clothing_items.name LIKE ?"
        args.append(f"%{filters['q']}%")

    for key, column in (
        ("item_type", "clothing_items.item_type"),
        ("style", "clothing_items.style"),
        ("color_id", "clothing_items.color_id"),
        ("category_id", "clothing_items.category_id"),
        ("available", "clothing_items.available"),
    ):
        value = filters.get(key)
        if value not in (None, ""):
            sql += f" AND {column} = ?"
            args.append(value)

    sql += " ORDER BY clothing_items.name COLLATE NOCASE"
    return get_db().execute(sql, args).fetchall()