from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

from core.db import get_db
from core.helpers import login_required
from features.catalog.models import visible_categories, visible_colors
from features.clothing_inventory import clothing_bp
from features.clothing_inventory.forms import item_errors
from features.clothing_inventory.models import get_item, list_items
from features.clothing_inventory.services import (
    delete_photo,
    save_photo,
    validate_catalog_choices,
)


def form_context(user_id, item=None):
    item_type = request.form.get(
        "item_type",
        item["item_type"] if item else "Top",
    )
    return {
        "item": item,
        "errors": {},
        "colors": visible_colors(),
        "categories": visible_categories(user_id, item_type),
        "selected_item_type": item_type,
    }


@clothing_bp.get("/")
@login_required
def index():
    filters = {
        "q": request.args.get("q", "").strip(),
        "item_type": request.args.get("item_type", ""),
        "style": request.args.get("style", ""),
        "color_id": request.args.get("color_id", ""),
        "category_id": request.args.get("category_id", ""),
        "available": request.args.get("available", ""),
    }

    items = list_items(session["user_id"], filters)
    return render_template(
        "clothing_list.html",
        items=items,
        colors=visible_colors(),
    )


@clothing_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    user_id = session["user_id"]
    context = form_context(user_id)

    if request.method == "POST":
        errors = item_errors(request.form)

        if not errors and not validate_catalog_choices(user_id, request.form):
            errors["catalog"] = (
                "The selected color or category is invalid for this item."
            )

        photo_name = None

        if not errors:
            try:
                photo_name = save_photo(request.files.get("photo"))
            except ValueError as error:
                errors["photo"] = str(error)

        if not errors:
            db = get_db()
            db.execute(
                """
                INSERT INTO clothing_items (
                    user_id, name, photo, item_type, style,
                    color_id, category_id, available
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (
                    user_id,
                    request.form["name"].strip(),
                    photo_name,
                    request.form["item_type"],
                    request.form["style"],
                    request.form["color_id"],
                    request.form["category_id"],
                ),
            )
            db.commit()
            flash("Clothing item added.", "success")
            return redirect(url_for("clothing.index"))

        context = form_context(user_id)
        context["errors"] = errors
        context["values"] = request.form

    return render_template("clothing_form.html", **context)


@clothing_bp.get("/<int:item_id>")
@login_required
def detail(item_id):
    item = get_item(session["user_id"], item_id)
    if item is None:
        abort(404)

    return render_template("clothing_detail.html", item=item)


@clothing_bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit(item_id):
    user_id = session["user_id"]
    item = get_item(user_id, item_id)

    if item is None:
        abort(404)

    context = form_context(user_id, item)

    if request.method == "POST":
        errors = item_errors(request.form)

        if not errors and not validate_catalog_choices(user_id, request.form):
            errors["catalog"] = (
                "The selected color or category is invalid for this item."
            )

        new_photo = None

        if not errors:
            try:
                new_photo = save_photo(request.files.get("photo"))
            except ValueError as error:
                errors["photo"] = str(error)

        if not errors:
            db = get_db()
            photo_name = new_photo or item["photo"]

            db.execute(
                """
                UPDATE clothing_items
                SET name = ?, photo = ?, item_type = ?, style = ?,
                    color_id = ?, category_id = ?
                WHERE id = ? AND user_id = ?
                """,
                (
                    request.form["name"].strip(),
                    photo_name,
                    request.form["item_type"],
                    request.form["style"],
                    request.form["color_id"],
                    request.form["category_id"],
                    item_id,
                    user_id,
                ),
            )
            db.commit()

            if new_photo:
                delete_photo(item["photo"])

            flash("Clothing item updated.", "success")
            return redirect(url_for("clothing.detail", item_id=item_id))

        context = form_context(user_id, item)
        context["errors"] = errors
        context["values"] = request.form

    return render_template("clothing_form.html", **context)


@clothing_bp.post("/<int:item_id>/availability")
@login_required
def availability(item_id):
    value = 1 if request.form.get("available") == "1" else 0

    get_db().execute(
        """
        UPDATE clothing_items
        SET available = ?
        WHERE id = ? AND user_id = ?
        """,
        (value, item_id, session["user_id"]),
    )
    get_db().commit()

    return redirect(url_for("clothing.detail", item_id=item_id))


@clothing_bp.post("/<int:item_id>/delete")
@login_required
def delete(item_id):
    item = get_item(session["user_id"], item_id)

    if item is None:
        abort(404)

    db = get_db()
    db.execute(
        "DELETE FROM clothing_items WHERE id = ? AND user_id = ?",
        (item_id, session["user_id"]),
    )
    db.commit()
    delete_photo(item["photo"])

    flash("Clothing item deleted.", "success")
    return redirect(url_for("clothing.index"))


@clothing_bp.get("/uploads/<filename>")
@login_required
def photo(filename):
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filename,
    )