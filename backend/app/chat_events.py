from flask import request

from .auth import user_from_token
from .extensions import db
from .models import ChatMessage

CHAT_MENU_CODE = "chat"
MAX_CONTENT_LENGTH = 500

# sid -> {"username": ..., "displayName": ...}
online_users = {}


def online_list():
    """在线成员列表：同一用户多标签页/多连接只算一个人。"""
    unique = {}
    for user in online_users.values():
        unique.setdefault(user["username"], user)
    return sorted(unique.values(), key=lambda user: user["username"])


def refresh_online_profile(username, display_name):
    """用户改昵名后，同步所有在线连接上的展示名（不靠重新连接）。"""
    for entry in online_users.values():
        if entry["username"] == username:
            entry["displayName"] = display_name


def _token_from(auth_payload):
    if isinstance(auth_payload, dict):
        token = auth_payload.get("token")
        if token:
            return token
    return request.args.get("token", "")


def init_chat_events(socketio):
    """注册聊天室相关 socket 事件（同一进程只注册一次）。"""
    online_users.clear()

    @socketio.on("connect")
    def handle_connect(auth=None):
        user = user_from_token(_token_from(auth))
        if user is None:
            return False
        if not any(menu.code == CHAT_MENU_CODE for menu in user.menus):
            return False

        online_users[request.sid] = {
            "username": user.username,
            "displayName": user.display_name,
        }
        socketio.emit("online_users", online_list())
        return True

    @socketio.on("disconnect")
    def handle_disconnect():
        online_users.pop(request.sid, None)
        socketio.emit("online_users", online_list())

    @socketio.on("chat_message")
    def handle_chat_message(payload):
        sender = online_users.get(request.sid)
        if sender is None:
            return False

        raw = payload.get("content") if isinstance(payload, dict) else None
        content = raw.strip() if isinstance(raw, str) else ""
        if not content:
            return False

        message = ChatMessage(
            username=sender["username"],
            display_name=sender["displayName"],
            content=content[:MAX_CONTENT_LENGTH],
        )
        db.session.add(message)
        db.session.commit()

        socketio.emit("chat_message", message.to_dict())
        return True
