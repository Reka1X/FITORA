from flask import Blueprint

user_profile_bp = Blueprint(
    "user_profile",
    __name__,
    template_folder="templates",
)

from features.user_profile import routes  # noqa: E402,F401