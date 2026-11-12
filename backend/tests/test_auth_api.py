def test_login_returns_token_and_user_profile(client):
    response = client.post(
        "/api/auth/login", json={"username": "admin", "password": "admin123"}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["code"] == 0

    data = body["data"]
    assert isinstance(data["token"], str) and data["token"]
    assert data["user"]["username"] == "admin"
    assert data["user"]["displayName"] == "系统管理员"


def test_login_rejects_wrong_password(client):
    response = client.post(
        "/api/auth/login", json={"username": "admin", "password": "wrong-password"}
    )

    assert response.status_code == 401
    assert response.get_json()["code"] != 0


def test_login_rejects_unknown_user(client):
    response = client.post(
        "/api/auth/login", json={"username": "nobody", "password": "admin123"}
    )

    assert response.status_code == 401


def test_menus_require_login(client):
    response = client.get("/api/menus")

    assert response.status_code == 401
    assert response.get_json()["code"] != 0


def test_menus_reject_invalid_token(client):
    response = client.get("/api/menus", headers={"Authorization": "Bearer not-a-token"})

    assert response.status_code == 401


def test_admin_gets_all_menus(client, admin_headers):
    menus = client.get("/api/menus", headers=admin_headers).get_json()["data"]

    assert [menu["code"] for menu in menus] == ["system", "analysis", "login-log", "chat"]


def test_analyst_only_gets_assigned_menus(client, analyst_headers):
    menus = client.get("/api/menus", headers=analyst_headers).get_json()["data"]

    assert [menu["code"] for menu in menus] == ["analysis", "chat"]
