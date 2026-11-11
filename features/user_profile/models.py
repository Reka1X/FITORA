from werkzeug.security import check_password_hash, generate_password_hash

from core.db import get_db


class User:
    def __init__(self, row):
        self.id = row["id"]
        self.full_name = row["full_name"]
        self.email = row["email"]
        self.profile_picture = row["profile_picture"]

    def get_profile_details(self):
        return {
            "full_name": self.full_name,
            "email": self.email,
        }

    def get_permissions(self):
        return {"manage_own_profile": True}

    @staticmethod
    def get_by_id(user_id):
        row = get_db().execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return StandardUser(row) if row else None

    @staticmethod
    def get_by_email(email):
        row = get_db().execute(
            "SELECT * FROM users WHERE email = ?",
            (email.strip().lower(),),
        ).fetchone()
        return StandardUser(row) if row else None

    @staticmethod
    def create(full_name, email, password):
        db = get_db()
        try:
            cursor = db.execute(
                """
                INSERT INTO users (full_name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (
                    full_name.strip(),
                    email.strip().lower(),
                    generate_password_hash(password),
                ),
            )
            db.commit()
            return cursor.lastrowid
        except Exception:
            db.rollback()
            return None

    @staticmethod
    def authenticate(email, password):
        row = get_db().execute(
            "SELECT * FROM users WHERE email = ?",
            (email.strip().lower(),),
        ).fetchone()

        if row and check_password_hash(row["password_hash"], password):
            return StandardUser(row)

        return None


class StandardUser(User):
    pass