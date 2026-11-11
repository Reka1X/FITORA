from flask import Blueprint

calendar_bp = Blueprint(
    "calendar",
    __name__,
    template_folder="templates",
)

from features.outfit_calendar import routes  # noqa: E402,F401