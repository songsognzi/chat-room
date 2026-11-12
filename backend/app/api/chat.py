from flask import Blueprint, jsonify, request

from ..auth import current_user, login_required, require_menu
from ..chat_events import CHAT_MENU_CODE, MAX_CONTENT_LENGTH
from ..extensions import db, socketio
from ..models import ChatMessage

chat_bp = Blueprint("chat", __name__)


@chat_bp.get("/chat/messages")
@login_required
@require_menu(CHAT_MENU_CODE)
def list_messages():
    """返回最近 50 条聊天记录（按时间正序），用于进入聊天室时回填历史。"""
    messages = (
        db.session.query(ChatMessage).order_by(ChatMessage.id.desc()).limit(50).all()
    )
    messages.reverse()
    return jsonify({"code": 0, "message": "ok", "data": [message.to_dict() for message in messages]})


@chat_bp.post("/chat/messages")
@login_required
@require_menu(CHAT_MENU_CODE)
def create_message():
    """HTTP 发送消息（socket 之外的备用通道），发送后同样广播给在线用户。"""
    payload = request.get_json(silent=True) or {}
    raw = payload.get("content")
    content = raw.strip() if isinstance(raw, str) else ""
    if not content:
        return jsonify({"code": 1004, "message": "消息内容不能为空", "data": None}), 400

    user = current_user()
    message = ChatMessage(
        username=user.username,
        display_name=user.display_name,
        content=content[:MAX_CONTENT_LENGTH],
    )
    db.session.add(message)
    db.session.commit()

    socketio.emit("chat_message", message.to_dict())
    return jsonify({"code": 0, "message": "ok", "data": message.to_dict()})
