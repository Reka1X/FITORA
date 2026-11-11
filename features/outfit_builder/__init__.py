from flask import Blueprint

outfit_bp = Blueprint(
    "outfit",
    __name__,
    template_folder="templates",
)

from features.outfit_builder import routes  # noqa: E402,F401