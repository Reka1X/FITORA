from core.db import get_db


class Recommendation:
    recommendation_type = "occasion"

    def __init__(self, items):
        self.items = list(items)

    def calculate_score(self, style, occasion):
        raise NotImplementedError

    def explain_score(self, style, occasion, score):
        raise NotImplementedError


class ColorMatchRecommendation(Recommendation):
    recommendation_type = "color"

    def calculate_score(self, style, occasion):
        colors = {
            item["color"].casefold()
            for item in self.items
            if item["color"]
        }
        score = 70 if len(colors) <= 2 else 55
        if any(item["style"] == style for item in self.items):
            score += 15
        return min(score, 100)

    def explain_score(self, style, occasion, score):
        return (
            f"Color match: the selected items use a coordinated palette. "
            f"The requested style is {style}; occasion is {occasion}. "
            f"Final score: {score}/100."
        )


class OccasionMatchRecommendation(Recommendation):
    recommendation_type = "occasion"

    def calculate_score(self, style, occasion):
        score = 40
        if any(item["style"] == style for item in self.items):
            score += 20

        roles = {item["item_type"] for item in self.items}
        if occasion in ("Work", "Formal event"):
            role_match = (
                {"Top", "Bottom", "Shoes"}.issubset(roles)
                or {"One-piece", "Shoes"}.issubset(roles)
            )
        elif occasion == "Sport":
            role_match = {"Top", "Bottom"}.issubset(roles)
        else:
            role_match = (
                {"Top", "Bottom"}.issubset(roles)
                or "One-piece" in roles
            )

        if role_match:
            score += 25

        colors = {
            item["color"].casefold()
            for item in self.items
            if item["color"]
        }
        if len(colors) <= 2:
            score += 15

        return min(score, 100)

    def explain_score(self, style, occasion, score):
        return (
            f"Occasion match: checked clothing-role coverage for {occasion}, "
            f"your requested {style} style, and color coordination. "
            f"Final score: {score}/100."
        )


class CapsuleRecommendation(Recommendation):
    recommendation_type = "capsule"

    def calculate_score(self, style, occasion):
        roles = {item["item_type"] for item in self.items}
        score = 40

        if len(roles) >= 3:
            score += 25
        elif len(roles) >= 2:
            score += 15

        matching_styles = sum(item["style"] == style for item in self.items)
        if matching_styles:
            score += 20

        colors = {
            item["color"].casefold()
            for item in self.items
            if item["color"]
        }
        if len(colors) <= 3:
            score += 15

        return min(score, 100)

    def explain_score(self, style, occasion, score):
        combo_count = max(0, len(self.items) - 1)
        return (
            f"Capsule suggestion: selected versatile pieces across clothing "
            f"roles that can form multiple combinations (at least "
            f"{combo_count} pairings). Style: {style}; occasion: {occasion}. "
            f"Final score: {score}/100."
        )


def list_for_user(user_id):
    return get_db().execute(
        """
        SELECT * FROM recommendations
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    ).fetchall()


def get_for_user(user_id, recommendation_id):
    return get_db().execute(
        """
        SELECT * FROM recommendations
        WHERE id = ? AND user_id = ?
        """,
        (recommendation_id, user_id),
    ).fetchone()


def create_recommendation(user_id, title, kind, occasion, style, score, explanation, items):
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO recommendations
            (user_id, title, recommendation_type, occasion, style, score, explanation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, title, kind, occasion, style, score, explanation),
    )
    recommendation_id = cursor.lastrowid

    for item in items:
        db.execute(
            """
            INSERT INTO recommendation_items
                (recommendation_id, item_name, item_type, style, color, category)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                recommendation_id,
                item["name"],
                item["item_type"],
                item["style"],
                item["color"],
                item["category"],
            ),
        )

    db.commit()
    return recommendation_id


def items_for_recommendation(recommendation_id):
    return get_db().execute(
        """
        SELECT * FROM recommendation_items
        WHERE recommendation_id = ?
        ORDER BY item_name
        """,
        (recommendation_id,),
    ).fetchall()