from core.db import get_db


class Outfit:
    def __init__(self, items):
        self.items = list(items)

    def compatibility_score(self, items=None):
        selected = items if items is not None else self.items
        return min(100, 50 + 10 * len(selected))


class CasualOutfit(Outfit):
    pass


class FormalOutfit(Outfit):
    pass


class SportOutfit(Outfit):
    pass


OUTFIT_CLASSES = {
    "Casual": CasualOutfit,
    "Formal": FormalOutfit,
    "Sport": SportOutfit,
}


def list_for_user(user_id):
    return get_db().execute(
        """
        SELECT * FROM outfits
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    ).fetchall()


def get_for_user(user_id, outfit_id):
    return get_db().execute(
        """
        SELECT * FROM outfits
        WHERE id = ? AND user_id = ?
        """,
        (outfit_id, user_id),
    ).fetchone()


def items_for_outfit(outfit_id):
    return get_db().execute(
        """
        SELECT * FROM outfit_items
        WHERE outfit_id = ?
        ORDER BY item_name
        """,
        (outfit_id,),
    ).fetchall()


def outfit_class(outfit_type, items):
    return OUTFIT_CLASSES.get(outfit_type, Outfit)(items)