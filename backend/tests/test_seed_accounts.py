import pytest

NEW_ACCOUNTS = [
    ("zhouyuyan", "周雨嫣"),
    ("ssz", "宋宋子"),
]


@pytest.mark.parametrize("username,display_name", NEW_ACCOUNTS)
def test_new_account_can_login(client, username, display_name):
    response = client.post(
        "/api/auth/login", json={"username": username, "password": "1314520"}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["code"] == 0
    assert body["data"]["user"]["username"] == username
    assert body["data"]["user"]["displayName"] == display_name


@pytest.mark.parametrize("username,display_name", NEW_ACCOUNTS)
def test_new_account_gets_analysis_and_chat_menus(client, username, display_name):
    token = client.post(
        "/api/auth/login", json={"username": username, "password": "1314520"}
    ).get_json()["data"]["token"]

    menus = client.get("/api/menus", headers={"Authorization": "Bearer " + token}).get_json()["data"]

    assert [menu["code"] for menu in menus] == ["analysis", "chat"]


def test_new_account_rejects_wrong_password(client):
    response = client.post(
        "/api/auth/login", json={"username": "zhouyuyan", "password": "1234567"}
    )

    assert response.status_code == 401
