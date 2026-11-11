ITEM_TYPES = ("Top", "Bottom", "One-piece", "Shoes")
STYLES = ("Casual", "Formal", "Street")


def item_errors(form):
    errors = {}

    if not form.get("name", "").strip():
        errors["name"] = "Enter an item name."

    if form.get("item_type") not in ITEM_TYPES:
        errors["item_type"] = "Choose a valid item type."

    if form.get("style") not in STYLES:
        errors["style"] = "Choose a valid style."

    if not form.get("color_id"):
        errors["color_id"] = "Choose a color."

    if not form.get("category_id"):
        errors["category_id"] = "Choose a category."

    return errors