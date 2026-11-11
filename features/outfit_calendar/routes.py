import sqlite3
from datetime import date

from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from core.db import get_db
from core.helpers import login_required
from features.outfit_calendar import calendar_bp
from features.outfit_calendar.forms import SCHEDULE_TYPES, schedule_errors
from features.outfit_calendar.models import get_for_user, list_for_user


def user_outfits(user_id):
    return get_db().execute(
        """
        SELECT id, name, outfit_type
        FROM outfits
        WHERE user_id = ?
        ORDER BY name COLLATE NOCASE
        """,
        (user_id,),
    ).fetchall()


@calendar_bp.get("/")
@login_required
def index():
    schedules = list_for_user(session["user_id"])
    return render_template(
        "calendar.html",
        schedules=schedules,
    )


@calendar_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    user_id = session["user_id"]
    outfits = user_outfits(user_id)
    errors = {}

    if request.method == "POST":
        errors = schedule_errors(request.form)

        outfit_id = request.form.get("outfit_id", type=int)
        owned_outfit = get_db().execute(
            "SELECT id FROM outfits WHERE id = ? AND user_id = ?",
            (outfit_id, user_id),
        ).fetchone()

        if not owned_outfit:
            errors["outfit_id"] = "Choose one of your saved outfits."

        if not errors:
            db = get_db()
            try:
                db.execute(
                    """
                    INSERT INTO outfit_schedules
                        (user_id, outfit_id, planned_date, schedule_type, note)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        outfit_id,
                        request.form["planned_date"],
                        request.form["schedule_type"],
                        request.form.get("note", "").strip(),
                    ),
                )
                db.commit()
                flash("Outfit scheduled.", "success")
                return redirect(url_for("calendar.index"))
            except sqlite3.IntegrityError:
                errors["planned_date"] = (
                    "That outfit is already scheduled for that date."
                )

    return render_template(
        "schedule_outfit.html",
        outfits=outfits,
        errors=errors,
        schedule=None,
        schedule_types=SCHEDULE_TYPES,
    )


@calendar_bp.get("/<int:schedule_id>")
@login_required
def detail(schedule_id):
    schedule = get_for_user(session["user_id"], schedule_id)

    if schedule is None:
        abort(404)

    return render_template(
        "schedule_detail.html",
        schedule=schedule,
    )


@calendar_bp.route("/<int:schedule_id>/edit", methods=["GET", "POST"])
@login_required
def edit(schedule_id):
    user_id = session["user_id"]
    schedule = get_for_user(user_id, schedule_id)

    if schedule is None:
        abort(404)

    outfits = user_outfits(user_id)
    errors = {}

    if request.method == "POST":
        errors = schedule_errors(request.form)

        outfit_id = request.form.get("outfit_id", type=int)
        owned_outfit = get_db().execute(
            "SELECT id FROM outfits WHERE id = ? AND user_id = ?",
            (outfit_id, user_id),
        ).fetchone()

        if not owned_outfit:
            errors["outfit_id"] = "Choose one of your saved outfits."

        if not errors:
            db = get_db()
            try:
                db.execute(
                    """
                    UPDATE outfit_schedules
                    SET outfit_id = ?, planned_date = ?,
                        schedule_type = ?, note = ?
                    WHERE id = ? AND user_id = ?
                    """,
                    (
                        outfit_id,
                        request.form["planned_date"],
                        request.form["schedule_type"],
                        request.form.get("note", "").strip(),
                        schedule_id,
                        user_id,
                    ),
                )
                db.commit()
                flash("Schedule updated.", "success")
                return redirect(
                    url_for("calendar.detail", schedule_id=schedule_id)
                )
            except sqlite3.IntegrityError:
                errors["planned_date"] = (
                    "That outfit is already scheduled for that date."
                )

    return render_template(
        "schedule_outfit.html",
        outfits=outfits,
        errors=errors,
        schedule=schedule,
        schedule_types=SCHEDULE_TYPES,
    )


@calendar_bp.post("/<int:schedule_id>/worn")
@login_required
def mark_worn(schedule_id):
    user_id = session["user_id"]
    schedule = get_for_user(user_id, schedule_id)

    if schedule is None:
        abort(404)

    db = get_db()
    try:
        db.execute(
            """
            INSERT INTO wear_history (user_id, outfit_id, worn_date)
            VALUES (?, ?, ?)
            """,
            (user_id, schedule.outfit_id, date.today().isoformat()),
        )
        db.commit()
        flash("Outfit added to wear history.", "success")
    except sqlite3.IntegrityError:
        flash("This outfit is already in today's wear history.", "warning")

    return redirect(url_for("calendar.detail", schedule_id=schedule_id))


@calendar_bp.post("/<int:schedule_id>/delete")
@login_required
def delete(schedule_id):
    db = get_db()
    db.execute(
        "DELETE FROM outfit_schedules WHERE id = ? AND user_id = ?",
        (schedule_id, session["user_id"]),
    )
    db.commit()
    flash("Schedule deleted.", "success")
    return redirect(url_for("calendar.index"))


@calendar_bp.get("/history")
@login_required
def history():
    rows = get_db().execute(
        """
        SELECT
            history.worn_date,
            outfits.name AS outfit_name,
            outfits.outfit_type
        FROM wear_history AS history
        JOIN outfits ON outfits.id = history.outfit_id
        WHERE history.user_id = ?
        ORDER BY history.worn_date DESC
        """,
        (session["user_id"],),
    ).fetchall()

    return render_template(
        "wear_history.html",
        history=rows,
    )