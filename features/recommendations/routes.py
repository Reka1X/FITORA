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
from features.recommendations import recommendations_bp
from features.recommendations.engine import generate
from features.recommendations.forms import preference_errors
from features.recommendations.models import (
    create_recommendation,
    get_for_user,
    items_for_recommendation,
    list_for_user,
)


@recommendations_bp.get("/")
@login_required
def index():
    recommendations = list_for_user(session["user_id"])
    return render_template(
        "recommendation_list.html",
        recommendations=recommendations,
    )


@recommendations_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    errors = {}

    if request.method == "POST":
        errors = preference_errors(request.form)

        items = get_db().execute(
            """
            SELECT
                clothing_items.*,
                colors.label AS color,
                categories.label AS category
            FROM clothing_items
            LEFT JOIN catalog_entries AS colors
                ON colors.id = clothing_items.color_id
            LEFT JOIN catalog_entries AS categories
                ON categories.id = clothing_items.category_id
            WHERE clothing_items.user_id = ?
              AND clothing_items.available = 1
            ORDER BY clothing_items.name
            """,
            (session["user_id"],),
        ).fetchall()

        if len(items) < 2:
            errors["items"] = "Add at least two available clothing items first."

        if not errors:
            result = generate(
                items,
                request.form["recommendation_type"],
                request.form["style"],
                request.form["occasion"],
            )

            if result["score"] < 60:
                errors["score"] = (
                    "This suggestion scored below 60/100. "
                    "Try another style or add more varied clothing."
                )
            else:
                recommendation_id = create_recommendation(
                    user_id=session["user_id"],
                    title=result["title"],
                    kind=result["type"],
                    occasion=request.form["occasion"],
                    style=request.form["style"],
                    score=result["score"],
                    explanation=result["explanation"],
                    items=result["items"],
                )
                flash("Recommendation created.", "success")
                return redirect(
                    url_for(
                        "recommendations.detail",
                        recommendation_id=recommendation_id,
                    )
                )

    return render_template(
        "recommendation_form.html",
        errors=errors,
        recommendation_types=("Color match", "Occasion match", "Capsule"),
        occasions=("Everyday", "Work", "Formal event", "Sport"),
        styles=("Casual", "Formal", "Street"),
    )


@recommendations_bp.get("/<int:recommendation_id>")
@login_required
def detail(recommendation_id):
    recommendation = get_for_user(
        session["user_id"],
        recommendation_id,
    )

    if recommendation is None:
        abort(404)

    items = items_for_recommendation(recommendation_id)

    return render_template(
        "recommendation_detail.html",
        recommendation=recommendation,
        items=items,
    )


@recommendations_bp.post("/<int:recommendation_id>/delete")
@login_required
def delete(recommendation_id):
    db = get_db()
    db.execute(
        "DELETE FROM recommendations WHERE id = ? AND user_id = ?",
        (recommendation_id, session["user_id"]),
    )
    db.commit()
    flash("Recommendation deleted.", "success")
    return redirect(url_for("recommendations.index"))