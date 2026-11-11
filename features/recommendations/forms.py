RECOMMENDATION_TYPES = ("Color match", "Occasion match", "Capsule")
OCCASIONS = ("Everyday", "Work", "Formal event", "Sport")
STYLES = ("Casual", "Formal", "Street")


def preference_errors(form):
    errors = {}

    if form.get("recommendation_type") not in RECOMMENDATION_TYPES:
        errors["recommendation_type"] = "Choose a recommendation type."

    if form.get("occasion") not in OCCASIONS:
        errors["occasion"] = "Choose an occasion."

    if form.get("style") not in STYLES:
        errors["style"] = "Choose a style."

    return errors