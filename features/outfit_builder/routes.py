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
from features.outfit_builder import outfit_bp
from features.outfit_builder.forms import outfit_errors
from features.outfit_builder.models import (
    get_for_user,
    items_for_outfit,
    list_for_user,
    outfit_class,
)


def available_items(user_id):
    return get_db().execute(
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
        ORDER BY clothing_items.name COLLATE NOCASE
        """,
        (user_id,),
    ).fetchall()


def save_outfit(user_id, form, selected_ids, outfit_id=None):
    db = get_db()
    selected_ids = list(dict.fromkeys(selected_ids))

    if len(selected_ids) < 2:
        return "Choose at least two distinct clothing items."

    placeholders = ",".join("?" for _ in selected_ids)
    selected = db.execute(
        f"""
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
          AND clothing_items.id IN ({placeholders})
        """,
        [user_id, *selected_ids],
    ).fetchall()

    if len(selected) != len(selected_ids):
        return "Selected items must belong to you and be available."

    if outfit_id is None:
        cursor = db.execute(
            """
            INSERT INTO outfits (user_id, name, outfit_type, description)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                form["name"].strip(),
                form["outfit_type"],
                form.get("description", "").strip(),
            ),
        )
        outfit_id = cursor.lastrowid
    else:
        db.execute(
            """
            UPDATE outfits
            SET name = ?, outfit_type = ?, description = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                form["name"].strip(),
                form["outfit_type"],
                form.get("description", "").strip(),
                outfit_id,
                user_id,
            ),
        )
        db.execute(
            "DELETE FROM outfit_items WHERE outfit_id = ?",
            (outfit_id,),
        )

    # Snapshots preserve how the saved outfit looked even if wardrobe records change.
    for item in selected:
        db.execute(
            """
            INSERT INTO outfit_items (
                outfit_id, clothing_item_id, item_name, item_type,
                style, color, category
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                outfit_id,
                item["id"],
                item["name"],
                item["item_type"],
                item["style"],
                item["color"],
                item["category"],
            ),
        )

    db.commit()
    return outfit_id


@outfit_bp.get("/")
@login_required
def index():
    outfits = list_for_user(session["user_id"])
    return render_template(
        "outfit_list.html",
        outfits=outfits,
    )


@outfit_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    user_id = session["user_id"]
    wardrobe = available_items(user_id)
    errors = {}
    selected_ids = []

    if request.method == "POST":
        errors = outfit_errors(request.form)
        selected_ids = request.form.getlist("item_ids")

        if not errors:
            result = save_outfit(user_id, request.form, selected_ids)

            if isinstance(result, int):
                flash("Outfit saved.", "success")
                return redirect(url_for("outfit.detail", outfit_id=result))

            errors["items"] = result

    return render_template(
        "outfit_form.html",
        outfit=None,
        wardrobe=wardrobe,
        errors=errors,
        selected_ids=selected_ids,
    )


@outfit_bp.get("/<int:outfit_id>")
@login_required
def detail(outfit_id):
    user_id = session["user_id"]
    outfit = get_for_user(user_id, outfit_id)

    if outfit is None:
        abort(404)

    items = items_for_outfit(outfit_id)
    model = outfit_class(outfit["outfit_type"], items)
    score = model.compatibility_score()

    return render_template(
        "outfit_detail.html",
        outfit=outfit,
        items=items,
        compatibility_score=score,
    )


@outfit_bp.route("/<int:outfit_id>/edit", methods=["GET", "POST"])
@login_required
def edit(outfit_id):
    user_id = session["user_id"]
    outfit = get_for_user(user_id, outfit_id)

    if outfit is None:
        abort(404)

    wardrobe = available_items(user_id)
    errors = {}

    existing = items_for_outfit(outfit_id)
    selected_ids = [
        str(item["clothing_item_id"])
        for item in existing
        if item["clothing_item_id"] is not None
    ]

    if request.method == "POST":
        errors = outfit_errors(request.form)
        selected_ids = request.form.getlist("item_ids")

        if not errors:
            result = save_outfit(
                user_id,
                request.form,
                selected_ids,
                outfit_id=outfit_id,
            )

            if isinstance(result, int):
                flash("Outfit updated.", "success")
                return redirect(
                    url_for("outfit.detail", outfit_id=outfit_id)
                )

            errors["items"] = result

    return render_template(
        "outfit_form.html",
        outfit=outfit,
        wardrobe=wardrobe,
        errors=errors,
        selected_ids=selected_ids,
    )


@outfit_bp.post("/<int:outfit_id>/delete")
@login_required
def delete(outfit_id):
    db = get_db()

    # The user_id condition prevents deleting another user's outfit.
    db.execute(
        "DELETE FROM outfits WHERE id = ? AND user_id = ?",
        (outfit_id, session["user_id"]),
    )
    db.commit()

    flash("Outfit deleted.", "success")
    return redirect(url_for("outfit.index"))
