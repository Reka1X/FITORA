import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from core.db import get_db
from features.catalog.models import valid_category


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def validate_catalog_choices(user_id, form):
    db = get_db()
    item_type = form.get("item_type", "")
    category_id = form.get("category_id", type=int)
    color_id = form.get("color_id", type=int)

    category_is_valid = valid_category(
        user_id,
        category_id,
        item_type,
    )

    color_is_valid = db.execute(
        """
        SELECT id FROM catalog_entries
        WHERE id = ?
          AND entry_type = 'color'
          AND user_id IS NULL
        """,
        (color_id,),
    ).fetchone()

    return category_is_valid and color_is_valid is not None


def save_photo(upload):
    if not upload or not upload.filename:
        return None

    filename = secure_filename(upload.filename)
    if "." not in filename:
        raise ValueError("Photo must be a JPG or PNG file.")

    extension = filename.rsplit(".", 1)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Photo must be a JPG or PNG file.")

    upload.stream.seek(0, os.SEEK_END)
    file_size = upload.stream.tell()
    upload.stream.seek(0)

    if file_size > current_app.config["MAX_CONTENT_LENGTH"]:
        raise ValueError("Photo must be 5 MB or smaller.")

    stored_name = f"{uuid.uuid4().hex}.{extension}"
    destination = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        stored_name,
    )
    upload.save(destination)
    return stored_name


def delete_photo(filename):
    if not filename:
        return

    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if os.path.isfile(path):
        os.remove(path)