from flask import Blueprint

catalog_bp = Blueprint(
    "catalog",
    __name__,
    template_folder="templates",
)

from features.catalog import routes  # noqa: E402,F401