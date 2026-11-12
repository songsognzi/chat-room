from flask import Blueprint, jsonify, request

from ..auth import create_token, current_user, login_required
from ..chat_events import online_list, refresh_online_profile
from ..extensions import db, socketio
from ..models import LoginLog, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

NICKNAME_MAX_LENGTH = 32


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    user = db.session.query(User).filter_by(username=username).one_or_none()
    if user is None or not user.check_password(password):
        return jsonify({"code": 1001, "message": "用户名或密码错误", "data": None}), 401

    db.session.add(
        LoginLog(
            username=user.username,
            ip=request.remote_addr or "",
            user_agent=(request.user_agent.string or "")[:255],
            status="success",
        )
    )
    db.session.commit()

    return jsonify(
        {
            "code": 0,
            "message": "ok",
            "data": {"token": create_token(user), "user": user.to_dict()},
        }
    )


@auth_bp.put("/profile")
@login_required
def update_profile():
    """修改当前登录用户自己的昵称。"""
    payload = request.get_json(silent=True) or {}
    raw = payload.get("displayName")
    display_name = raw.strip() if isinstance(raw, str) else ""

    if not display_name:
        return jsonify({"code": 1005, "message": "昵称不能为空", "data": None}), 400

    if len(display_name) > NICKNAME_MAX_LENGTH:
        return jsonify(
            {"code": 1006, "message": f"昵称最多 {NICKNAME_MAX_LENGTH} 个字符", "data": None}
        ), 400

    user = current_user()
    user.display_name = display_name
    db.session.commit()

    # 让在线列表立刻显示新昵称
    refresh_online_profile(user.username, user.display_name)
    socketio.emit("online_users", online_list())

    return jsonify({"code": 0, "message": "ok", "data": {"user": user.to_dict()}})
