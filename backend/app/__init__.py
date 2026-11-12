import os

from flask import Flask

from .api import api_bp
from .chat_events import init_chat_events
from .extensions import db, socketio
from .models import seed_default_data

DEFAULT_SECRET_KEY = "dev-only-secret-key-change-me"


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///" + app.instance_path.replace("\\", "/") + "/admin.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.environ.get("ADMIN_SECRET_KEY", DEFAULT_SECRET_KEY),
    )
    if config:
        app.config.update(config)

    app.json.ensure_ascii = False

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    socketio.init_app(app, async_mode="threading", cors_allowed_origins="*")
    init_chat_events(socketio)

    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()
        seed_default_data()

    return app
