from functools import wraps

from flask import current_app, g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from .extensions import db
from .models import User

TOKEN_MAX_AGE_SECONDS = 8 * 60 * 60


def _serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="auth-token")


def create_token(user):
    return _serializer().dumps({"uid": user.id})


def user_from_token(token):
    try:
        payload = _serializer().loads(token, max_age=TOKEN_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        return None
    return db.session.get(User, payload.get("uid"))


def _bearer_token():
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        return header[7:].strip()
    return ""


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        user = user_from_token(_bearer_token())
        if user is None:
            return jsonify({"code": 1002, "message": "未登录或登录已过期", "data": None}), 401
        g.current_user = user
        return view(*args, **kwargs)

    return wrapper


def current_user():
    return g.current_user


def require_menu(menu_code):
    """限定当前用户必须拥有某个菜单权限，需按序叠在 login_required 下方。"""

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if not any(menu.code == menu_code for menu in current_user().menus):
                return jsonify({"code": 1003, "message": "没有该菜单的访问权限", "data": None}), 403
            return view(*args, **kwargs)

        return wrapper

    return decorator
