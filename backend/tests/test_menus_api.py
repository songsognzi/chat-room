def test_menus_endpoint_returns_all_admin_menus(client, admin_headers):
    response = client.get("/api/menus", headers=admin_headers)

    assert response.status_code == 200
    body = response.get_json()
    assert body["code"] == 0
    menus = body["data"]
    assert [menu["name"] for menu in menus] == ["系统配置", "统计分析", "登录信息", "聊天室"]

    system_menu = menus[0]
    assert system_menu["code"] == "system"
    assert system_menu["path"] == "/system"
    assert system_menu["component"] == "system/index"

    analysis_menu = menus[1]
    assert analysis_menu["code"] == "analysis"
    assert analysis_menu["path"] == "/analysis"
    assert analysis_menu["component"] == "analysis/index"


def test_menus_endpoint_reads_from_database_ordered_by_sort(app, client, admin_headers):
    from app.extensions import db
    from app.models import Menu, User

    with app.app_context():
        menu = Menu(code="report", name="报表中心", path="/report", component="report/index", sort=99)
        admin = db.session.query(User).filter_by(username="admin").one()
        db.session.add(menu)
        db.session.flush()
        admin.menus.append(menu)
        db.session.commit()

    menus = client.get("/api/menus", headers=admin_headers).get_json()["data"]

    assert [menu["code"] for menu in menus] == ["system", "analysis", "login-log", "chat", "report"]


def test_seed_defaults_is_idempotent():
    from flask import Flask

    from app.extensions import db
    from app.models import Menu, User, seed_default_data

    flask_app = Flask(__name__)
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    flask_app.config["SECRET_KEY"] = "test"

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

        seed_default_data()
        seed_default_data()

        assert db.session.query(Menu).count() == 4
        assert db.session.query(User).count() == 4
