def test_default_config_can_serve_menus_after_login():
    from app import create_app as factory

    default_app = factory()
    client = default_app.test_client()

    token = client.post(
        "/api/auth/login", json={"username": "admin", "password": "admin123"}
    ).get_json()["data"]["token"]

    body = client.get("/api/menus", headers={"Authorization": "Bearer " + token}).get_json()

    assert [menu["code"] for menu in body["data"]] == ["system", "analysis", "login-log", "chat"]
