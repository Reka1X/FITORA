from flask import Blueprint

clothing_bp = Blueprint(
    "clothing",
    __name__,
    template_folder="templates",
)

from features.clothing_inventory import routes  # noqa: E402,F401