from datetime import datetime, timedelta

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db

DEFAULT_MENUS = [
    {"code": "system", "name": "系统配置", "path": "/system", "component": "system/index", "icon": "setting", "sort": 10},
    {"code": "analysis", "name": "统计分析", "path": "/analysis", "component": "analysis/index", "icon": "chart", "sort": 20},
    {"code": "login-log", "name": "登录信息", "path": "/login-info", "component": "login-info/index", "icon": "log", "sort": 30},
    {"code": "chat", "name": "聊天室", "path": "/chat", "component": "chat/index", "icon": "chat", "sort": 40},
]

DEFAULT_LOGIN_LOGS = [
    {"username": "admin", "ip": "10.12.3.21", "user_agent": "Chrome 141 / Windows 11", "status": "success", "minutes_ago": 8},
    {"username": "analyst", "ip": "10.12.3.58", "user_agent": "Chrome 141 / Windows 11", "status": "success", "minutes_ago": 36},
    {"username": "analyst", "ip": "10.12.7.14", "user_agent": "Edge 140 / macOS 14", "status": "failed", "minutes_ago": 95},
    {"username": "admin", "ip": "10.12.3.21", "user_agent": "Chrome 141 / Windows 11", "status": "success", "minutes_ago": 170},
    {"username": "guest", "ip": "10.12.9.3", "user_agent": "Firefox 139 / Ubuntu 24.04", "status": "failed", "minutes_ago": 240},
    {"username": "admin", "ip": "10.12.3.21", "user_agent": "Safari 18 / macOS 15", "status": "success", "minutes_ago": 480},
]

DEFAULT_USERS = [
    {
        "username": "admin",
        "password": "admin123",
        "display_name": "系统管理员",
        "menu_codes": ["system", "analysis", "login-log", "chat"],
    },
    {
        "username": "analyst",
        "password": "analyst123",
        "display_name": "数据分析员",
        "menu_codes": ["analysis", "chat"],
    },
    {
        "username": "zhouyuyan",
        "password": "1314520",
        "display_name": "周雨嫣",
        "menu_codes": ["analysis", "chat"],
    },
    {
        "username": "ssz",
        "password": "1314520",
        "display_name": "宋宋子",
        "menu_codes": ["analysis", "chat"],
    },
]

user_menus = db.Table(
    "user_menus",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("menu_id", db.Integer, db.ForeignKey("menus.id"), primary_key=True),
)


class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    path = db.Column(db.String(128), nullable=False)
    component = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(64), nullable=False, default="")
    sort = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "path": self.path,
            "component": self.component,
            "icon": self.icon,
            "sort": self.sort,
        }


class LoginLog(db.Model):
    __tablename__ = "login_logs"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    ip = db.Column(db.String(64), nullable=False, default="")
    user_agent = db.Column(db.String(255), nullable=False, default="")
    status = db.Column(db.String(16), nullable=False, default="success")
    login_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "ip": self.ip,
            "userAgent": self.user_agent,
            "status": self.status,
            "loginAt": self.login_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    display_name = db.Column(db.String(64), nullable=False, default="")
    content = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "displayName": self.display_name,
            "content": self.content,
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(64), nullable=False, default="")

    menus = db.relationship(
        "Menu",
        secondary=user_menus,
        lazy="selectin",
        order_by="Menu.sort",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "displayName": self.display_name,
        }


def seed_default_menus():
    """写入默认菜单，已存在的菜单不会重复插入。"""
    for item in DEFAULT_MENUS:
        exists = db.session.query(Menu.id).filter_by(code=item["code"]).first()
        if exists is None:
            db.session.add(Menu(**item))
    db.session.commit()


def seed_default_users():
    """写入默认账号并绑定各自可见的菜单，已存在的账号不重复插入。"""
    menus = {menu.code: menu for menu in db.session.query(Menu).all()}
    for item in DEFAULT_USERS:
        desired = [menus[code] for code in item["menu_codes"] if code in menus]
        user = db.session.query(User).filter_by(username=item["username"]).one_or_none()
        if user is None:
            user = User(username=item["username"], display_name=item["display_name"])
            user.set_password(item["password"])
            user.menus = desired
            db.session.add(user)
            continue
        # 已有账号：只补上配置里新增的菜单，不动手工调整过的授权
        for menu in desired:
            if menu not in user.menus:
                user.menus.append(menu)
    db.session.commit()


def seed_login_logs():
    """登录日志表为空时写入演示数据，便于登录信息页直接看到内容。"""
    if db.session.query(LoginLog.id).first() is not None:
        return

    now = datetime.now()
    for item in DEFAULT_LOGIN_LOGS:
        db.session.add(
            LoginLog(
                username=item["username"],
                ip=item["ip"],
                user_agent=item["user_agent"],
                status=item["status"],
                login_at=now - timedelta(minutes=item["minutes_ago"]),
            )
        )
    db.session.commit()


def seed_default_data():
    seed_default_menus()
    seed_default_users()
    seed_login_logs()
