from core.db import get_db


class OutfitSchedule:
    schedule_type = "Casual"

    def __init__(self, row):
        self.id = row["id"]
        self.user_id = row["user_id"]
        self.outfit_id = row["outfit_id"]
        self.planned_date = row["planned_date"]
        self.note = row["note"]
        self.outfit_name = row["outfit_name"]
        self.schedule_type = row["schedule_type"]

    def describe(self):
        return f"{self.outfit_name} planned for {self.planned_date}"


class CasualSchedule(OutfitSchedule):
    schedule_type = "Casual"

    def describe(self):
        return f"Casual outfit {self.outfit_name} planned for {self.planned_date}"


class WorkSchedule(OutfitSchedule):
    schedule_type = "Work"

    def describe(self):
        return f"Work outfit {self.outfit_name} planned for {self.planned_date}"


class EventSchedule(OutfitSchedule):
    schedule_type = "Event"

    def describe(self):
        return f"Event outfit {self.outfit_name} planned for {self.planned_date}"


SCHEDULE_CLASSES = {
    "Casual": CasualSchedule,
    "Work": WorkSchedule,
    "Event": EventSchedule,
}


def schedule_from_row(row):
    schedule_class = SCHEDULE_CLASSES.get(
        row["schedule_type"],
        OutfitSchedule,
    )
    return schedule_class(row)


def list_for_user(user_id):
    rows = get_db().execute(
        """
        SELECT
            schedules.*,
            outfits.name AS outfit_name
        FROM outfit_schedules AS schedules
        JOIN outfits ON outfits.id = schedules.outfit_id
        WHERE schedules.user_id = ?
        ORDER BY schedules.planned_date
        """,
        (user_id,),
    ).fetchall()

    return [schedule_from_row(row) for row in rows]


def get_for_user(user_id, schedule_id):
    row = get_db().execute(
        """
        SELECT
            schedules.*,
            outfits.name AS outfit_name
        FROM outfit_schedules AS schedules
        JOIN outfits ON outfits.id = schedules.outfit_id
        WHERE schedules.id = ? AND schedules.user_id = ?
        """,
        (schedule_id, user_id),
    ).fetchone()

    return schedule_from_row(row) if row else None