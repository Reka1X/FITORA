VALID_ITEM_TYPES = ("Top", "Bottom", "One-piece", "Shoes")


def category_errors(form):
    errors = {}

    label = " ".join(form.get("label", "").split())
    item_type = form.get("item_type", "")

    if not label:
        errors["label"] = "Enter a category name."

    if item_type not in VALID_ITEM_TYPES:
        errors["item_type"] = "Choose a valid item type."

    return errors