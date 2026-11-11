OUTFIT_TYPES = ("Casual", "Formal", "Sport")


def outfit_errors(form):
    errors = {}

    if not form.get("name", "").strip():
        errors["name"] = "Enter an outfit name."

    if form.get("outfit_type") not in OUTFIT_TYPES:
        errors["outfit_type"] = "Choose a valid outfit type."

    return errors