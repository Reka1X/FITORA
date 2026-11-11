import os

from flask import Flask, render_template

from config import Config
from core.db import close_db, init_db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.teardown_appcontext(close_db)

    from features.user_profile import user_profile_bp
    from features.catalog import catalog_bp
    from features.clothing_inventory import clothing_bp
    from features.outfit_builder import outfit_bp
    from features.recommendations import recommendations_bp
    from features.outfit_calendar import calendar_bp
    from dashboard import dashboard_bp

    app.register_blueprint(user_profile_bp)
    app.register_blueprint(catalog_bp, url_prefix="/catalog")
    app.register_blueprint(clothing_bp, url_prefix="/wardrobe")
    app.register_blueprint(outfit_bp, url_prefix="/outfits")
    app.register_blueprint(recommendations_bp, url_prefix="/recommendations")
    app.register_blueprint(calendar_bp, url_prefix="/calendar")
    app.register_blueprint(dashboard_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("500.html"), 500

    with app.app_context():
        init_db()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)