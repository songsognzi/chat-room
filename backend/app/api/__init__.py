from flask import Blueprint

from .auth import auth_bp
from .chat import chat_bp
from .login_logs import login_logs_bp
from .menus import menus_bp

api_bp = Blueprint("api", __name__)
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(menus_bp)
api_bp.register_blueprint(login_logs_bp)
api_bp.register_blueprint(chat_bp)
