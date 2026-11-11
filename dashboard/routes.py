from flask import render_template, session

from core.db import get_db
from core.helpers import login_required
from dashboard import dashboard_bp


@dashboard_bp.get("/")
@login_required
def index():
    db = get_db()
    user_id = session["user_id"]

    counts = {}
    tables = {
        "Clothing items": "clothing_items",
        "Outfits": "outfits",
        "Recommendations": "recommendations",
        "Scheduled outfits": "outfit_schedules",
    }

    for label, table in tables.items():
        counts[label] = db.execute(
            f"SELECT COUNT(*) AS total FROM {table} WHERE user_id = ?",
            (user_id,),
        ).fetchone()["total"]

    upcoming = db.execute(
        """
        SELECT schedules.planned_date, outfits.name
        FROM outfit_schedules AS schedules
        JOIN outfits ON outfits.id = schedules.outfit_id
        WHERE schedules.user_id = ?
          AND schedules.planned_date >= date('now')
        ORDER BY schedules.planned_date
        LIMIT 5
        """,
        (user_id,),
    ).fetchall()

    return render_template(
        "dashboard.html",
        counts=counts,
        upcoming=upcoming,
    )