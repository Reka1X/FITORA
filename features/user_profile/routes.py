from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from core.db import get_db
from core.helpers import login_required
from features.user_profile import user_profile_bp
from features.user_profile.forms import registration_errors
from features.user_profile.models import User


@user_profile_bp.route("/register", methods=["GET", "POST"])
def register():
    errors = {}

    if request.method == "POST":
        errors = registration_errors(request.form)

        if not errors:
            user_id = User.create(
                request.form["full_name"],
                request.form["email"],
                request.form["password"],
            )

            if user_id:
                session.clear()
                session["user_id"] = user_id
                return redirect(url_for("dashboard.index"))

            errors["email"] = "An account with that email already exists."

    return render_template("register.html", errors=errors)


@user_profile_bp.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        user = User.authenticate(
            request.form.get("email", ""),
            request.form.get("password", ""),
        )

        if user:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("dashboard.index"))

        error = "Email or password is incorrect."

    return render_template("login.html", error=error)


@user_profile_bp.post("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("user_profile.login"))


@user_profile_bp.get("/profile")
@login_required
def profile():
    user = User.get_by_id(session["user_id"])
    return render_template("profile.html", user=user)


@user_profile_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    db = get_db()
    user_id = session["user_id"]
    user = User.get_by_id(user_id)
    error = ""

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()

        other = db.execute(
            "SELECT id FROM users WHERE email = ? AND id <> ?",
            (email, user_id),
        ).fetchone()

        if not full_name or "@" not in email:
            error = "Enter a name and valid email address."
        elif other:
            error = "That email is already in use."
        else:
            db.execute(
                "UPDATE users SET full_name = ?, email = ? WHERE id = ?",
                (full_name, email, user_id),
            )
            db.commit()
            flash("Profile updated.", "success")
            return redirect(url_for("user_profile.profile"))

    return render_template("edit_profile.html", user=user, error=error)


@user_profile_bp.route("/profile/password", methods=["GET", "POST"])
@login_required
def change_password():
    db = get_db()
    error = ""

    if request.method == "POST":
        row = db.execute(
            "SELECT password_hash FROM users WHERE id = ?",
            (session["user_id"],),
        ).fetchone()

        new_password = request.form.get("new_password", "")
        current_password = request.form.get("current_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not check_password_hash(row["password_hash"], current_password):
            error = "Current password is incorrect."
        elif len(new_password) < 8 or new_password != confirm_password:
            error = "New passwords must match and be at least 8 characters."
        else:
            db.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (generate_password_hash(new_password), session["user_id"]),
            )
            db.commit()
            flash("Password changed.", "success")
            return redirect(url_for("user_profile.profile"))

    return render_template("change_password.html", error=error)