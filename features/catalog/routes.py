from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from core.db import get_db
from core.helpers import login_required
from features.catalog import catalog_bp
from features.catalog.forms import category_errors
from features.catalog.models import (
    get_entry,
    list_entries,
    visible_categories,
    visible_colors,
)
from features.catalog.services import (
    create_category,
    delete_category,
    update_category,
)


@catalog_bp.get("/")
@login_required
def index():
    entries = list_entries(
        user_id=session["user_id"],
        entry_type=request.args.get("entry_type", ""),
        item_type=request.args.get("item_type", ""),
        search=request.args.get("q", "").strip(),
    )
    return render_template("catalog_list.html", entries=entries)


@catalog_bp.route("/categories/new", methods=["GET", "POST"])
@login_required
def create():
    errors = {}

    if request.method == "POST":
        errors = category_errors(request.form)

        if not errors:
            success = create_category(
                session["user_id"],
                request.form["label"],
                request.form["item_type"],
            )

            if success:
                flash("Category created.", "success")
                return redirect(url_for("catalog.index"))

            errors["label"] = (
                "A category with that name is already available "
                "for this item type."
            )

    return render_template(
        "catalog_form.html",
        errors=errors,
        entry=None,
    )


@catalog_bp.route(
    "/categories/<int:entry_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit(entry_id):
    entry = get_entry(entry_id)

    # Shared entries and other users' entries cannot be edited.
    if (
        entry is None
        or entry["entry_type"] != "category"
        or entry["user_id"] != session["user_id"]
    ):
        flash("You can only edit your own categories.", "warning")
        return redirect(url_for("catalog.index"))

    errors = {}

    if request.method == "POST":
        errors = category_errors(request.form)

        if not errors:
            success = update_category(
                session["user_id"],
                entry_id,
                request.form["label"],
                request.form["item_type"],
            )

            if success:
                flash("Category updated.", "success")
                return redirect(url_for("catalog.index"))

            errors["label"] = (
                "That category name is already available "
                "for the selected item type."
            )

    return render_template(
        "catalog_form.html",
        errors=errors,
        entry=entry,
    )


@catalog_bp.post("/categories/<int:entry_id>/delete")
@login_required
def delete(entry_id):
    result = delete_category(session["user_id"], entry_id)

    if result == "deleted":
        flash("Category deleted.", "success")
    elif result == "in_use":
        flash("This category is used by clothing items and cannot be deleted.", "warning")
    else:
        flash("You can only delete your own categories.", "warning")

    return redirect(url_for("catalog.index"))


@catalog_bp.get("/options/<item_type>")
@login_required
def category_options(item_type):
    if item_type not in ("Top", "Bottom", "One-piece", "Shoes"):
        return "", 400

    categories = visible_categories(session["user_id"], item_type)
    return render_template(
        "partials/category_options.html",
        categories=categories,
    )


@catalog_bp.get("/colors/options")
@login_required
def color_options():
    return render_template(
        "partials/color_options.html",
        colors=visible_colors(),
    )