import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-development-key")
    DATABASE = os.environ.get(
        "FITORA_DATABASE",
        str(BASE_DIR / "instance" / "fitora.sqlite"),
    )
    UPLOAD_FOLDER = str(BASE_DIR / "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024