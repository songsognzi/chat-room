from flask import Blueprint, jsonify

from ..auth import login_required, require_menu
from ..extensions import db
from ..models import LoginLog

login_logs_bp = Blueprint("login_logs", __name__)


@login_logs_bp.get("/login-logs")
@login_required
@require_menu("login-log")
def list_login_logs():
    """返回最近的登录记录，供「登录信息」页面展示。"""
    logs = (
        db.session.query(LoginLog)
        .order_by(LoginLog.login_at.desc(), LoginLog.id.desc())
        .limit(50)
        .all()
    )
    return jsonify({"code": 0, "message": "ok", "data": [log.to_dict() for log in logs]})
