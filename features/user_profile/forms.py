import re


def valid_email(email):
    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email.strip(),
        )
    )


def registration_errors(form):
    errors = {}

    if not form.get("full_name", "").strip():
        errors["full_name"] = "Enter your full name."

    if not valid_email(form.get("email", "")):
        errors["email"] = "Enter a valid email address."

    if len(form.get("password", "")) < 8:
        errors["password"] = "Password must be at least 8 characters."

    if form.get("password") != form.get("confirm_password"):
        errors["confirm_password"] = "Passwords do not match."

    return errors