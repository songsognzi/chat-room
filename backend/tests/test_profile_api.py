def test_update_profile_requires_login(client):
    response = client.put("/api/auth/profile", json={"displayName": "新昵称"})

    assert response.status_code == 401


def test_update_profile_changes_nickname(client, admin_headers):
    response = client.put(
        "/api/auth/profile", json={"displayName": "  管理员小明  "}, headers=admin_headers
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["code"] == 0
    assert body["data"]["user"]["displayName"] == "管理员小明"


def test_update_profile_is_persisted(client, admin_headers):
    client.put("/api/auth/profile", json={"displayName": "持久化昵称"}, headers=admin_headers)

    # 重新登录拿到的是新昵称，说明落库了
    body = client.post(
        "/api/auth/login", json={"username": "admin", "password": "admin123"}
    ).get_json()

    assert body["data"]["user"]["displayName"] == "持久化昵称"


def test_update_profile_rejects_blank_nickname(client, admin_headers):
    response = client.put("/api/auth/profile", json={"displayName": "   "}, headers=admin_headers)

    assert response.status_code == 400
    assert response.get_json()["code"] != 0


def test_update_profile_rejects_too_long_nickname(client, admin_headers):
    response = client.put(
        "/api/auth/profile", json={"displayName": "昵" * 33}, headers=admin_headers
    )

    assert response.status_code == 400
    assert response.get_json()["code"] != 0


def test_update_profile_only_affects_current_user(client, admin_headers):
    client.put("/api/auth/profile", json={"displayName": "只改自己"}, headers=admin_headers)

    body = client.post(
        "/api/auth/login", json={"username": "analyst", "password": "analyst123"}
    ).get_json()

    assert body["data"]["user"]["displayName"] == "数据分析员"


def test_update_profile_refreshes_online_users(app, client, admin_token, admin_headers):
    from app.extensions import socketio

    admin_socket = socketio.test_client(app, auth={"token": admin_token})
    admin_socket.get_received()

    client.put("/api/auth/profile", json={"displayName": "在线新昵称"}, headers=admin_headers)

    events = [e for e in admin_socket.get_received() if e["name"] == "online_users"]
    assert events, "昵称修改后应广播最新的在线列表"
    assert [user["displayName"] for user in events[-1]["args"][0]] == ["在线新昵称"]

    admin_socket.disconnect()
