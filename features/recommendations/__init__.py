from flask import Blueprint

recommendations_bp = Blueprint(
    "recommendations",
    __name__,
    template_folder="templates",
)

from features.recommendations import routes  # noqa: E402,F401