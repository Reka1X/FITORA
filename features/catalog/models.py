from core.db import get_db


class CatalogEntry:
    def __init__(self, row):
        self.id = row["id"]
        self.label = row["label"]
        self.user_id = row["user_id"]
        self.entry_type = row["entry_type"]

    def normalized_label(self):
        return " ".join(self.label.split()).casefold()

    def describe_usage(self):
        return self.label


class CategoryEntry(CatalogEntry):
    def __init__(self, row):
        super().__init__(row)
        self.item_type = row["item_type"]

    def describe_usage(self):
        return f"Category for {self.item_type}"


class ColorEntry(CatalogEntry):
    def describe_usage(self):
        return "Clothing color"


def list_entries(user_id, entry_type="", item_type="", search=""):
    sql = """
        SELECT *
        FROM catalog_entries
        WHERE (user_id IS NULL OR user_id = ?)
    """
    args = [user_id]

    if entry_type:
        sql += " AND entry_type = ?"
        args.append(entry_type)

    if item_type and entry_type == "category":
        sql += " AND item_type = ?"
        args.append(item_type)

    if search:
        sql += " AND label LIKE ?"
        args.append(f"%{search}%")

    sql += " ORDER BY entry_type, label COLLATE NOCASE"
    return get_db().execute(sql, args).fetchall()


def get_entry(entry_id):
    return get_db().execute(
        "SELECT * FROM catalog_entries WHERE id = ?",
        (entry_id,),
    ).fetchone()


def visible_colors():
    return get_db().execute(
        """
        SELECT * FROM catalog_entries
        WHERE entry_type = 'color' AND user_id IS NULL
        ORDER BY label COLLATE NOCASE
        """
    ).fetchall()


def visible_categories(user_id, item_type):
    return get_db().execute(
        """
        SELECT * FROM catalog_entries
        WHERE entry_type = 'category'
          AND item_type = ?
          AND (user_id IS NULL OR user_id = ?)
        ORDER BY label COLLATE NOCASE
        """,
        (item_type, user_id),
    ).fetchall()


def valid_category(user_id, category_id, item_type):
    row = get_db().execute(
        """
        SELECT id FROM catalog_entries
        WHERE id = ?
          AND entry_type = 'category'
          AND item_type = ?
          AND (user_id IS NULL OR user_id = ?)
        """,
        (category_id, item_type, user_id),
    ).fetchone()
    return row is not None