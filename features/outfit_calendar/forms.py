from datetime import date


SCHEDULE_TYPES = ("Casual", "Work", "Event")


def schedule_errors(form):
    errors = {}

    if not form.get("outfit_id", "").isdigit():
        errors["outfit_id"] = "Choose an outfit."

    if form.get("schedule_type") not in SCHEDULE_TYPES:
        errors["schedule_type"] = "Choose a schedule type."

    try:
        date.fromisoformat(form.get("planned_date", ""))
    except ValueError:
        errors["planned_date"] = "Choose a valid date."

    return errors