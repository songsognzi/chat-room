from flask import Blueprint, jsonify

from ..auth import current_user, login_required

menus_bp = Blueprint("menus", __name__)


@menus_bp.get("/menus")
@login_required
def list_menus():
    """返回当前登录用户拥有的菜单，前端据此生成路由与侧边栏。"""
    menus = sorted(current_user().menus, key=lambda menu: (menu.sort, menu.id))
    return jsonify({"code": 0, "message": "ok", "data": [menu.to_dict() for menu in menus]})
