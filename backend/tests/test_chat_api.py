def test_chat_history_requires_login(client):
    assert client.get("/api/chat/messages").status_code == 401


def test_chat_history_requires_chat_menu(app, client):
    from app.extensions import db
    from app.models import User

    with app.app_context():
        user = User(username="nochat", display_name="无聊天权限")
        user.set_password("nochat123")
        db.session.add(user)
        db.session.commit()

    token = client.post(
        "/api/auth/login", json={"username": "nochat", "password": "nochat123"}
    ).get_json()["data"]["token"]

    response = client.get("/api/chat/messages", headers={"Authorization": "Bearer " + token})

    assert response.status_code == 403


def test_chat_history_returns_messages_in_time_order(client, admin_headers):
    client.post(
        "/api/chat/messages",
        json={"content": "第一条"},
        headers=admin_headers,
    )
    client.post(
        "/api/chat/messages",
        json={"content": "第二条"},
        headers=admin_headers,
    )

    body = client.get("/api/chat/messages", headers=admin_headers).get_json()

    assert body["code"] == 0
    contents = [message["content"] for message in body["data"]]
    assert contents[-2:] == ["第一条", "第二条"]
    assert set(body["data"][0].keys()) == {"id", "username", "displayName", "content", "createdAt"}


def test_chat_message_rejects_empty_content(client, admin_headers):
    response = client.post("/api/chat/messages", json={"content": "   "}, headers=admin_headers)

    assert response.status_code == 400
    assert response.get_json()["code"] != 0


def test_socket_connect_requires_valid_token(app):
    from app.extensions import socketio

    socket_client = socketio.test_client(app, auth={"token": "broken-token"})

    assert socket_client.is_connected() is False


def test_socket_connect_requires_chat_menu(app, client):
    from app.extensions import db, socketio
    from app.models import User

    with app.app_context():
        user = User(username="nochat2", display_name="无聊天权限2")
        user.set_password("nochat123")
        db.session.add(user)
        db.session.commit()

    token = client.post(
        "/api/auth/login", json={"username": "nochat2", "password": "nochat123"}
    ).get_json()["data"]["token"]

    socket_client = socketio.test_client(app, auth={"token": token})

    assert socket_client.is_connected() is False


def test_socket_connect_broadcasts_online_users(app, admin_token, analyst_token):
    from app.extensions import socketio

    admin_socket = socketio.test_client(app, auth={"token": admin_token})
    assert admin_socket.is_connected() is True

    admin_events = admin_socket.get_received()
    assert [event["name"] for event in admin_events] == ["online_users"]
    assert [user["username"] for user in admin_events[0]["args"][0]] == ["admin"]

    analyst_socket = socketio.test_client(app, auth={"token": analyst_token})
    analyst_events = analyst_socket.get_received()
    assert [user["username"] for user in analyst_events[0]["args"][0]] == ["admin", "analyst"]

    admin_socket.get_received()
    admin_socket.disconnect()
    analyst_socket.disconnect()


def test_online_users_deduplicates_same_user_with_multiple_connections(app, admin_token):
    from app.extensions import socketio

    first = socketio.test_client(app, auth={"token": admin_token})
    first.get_received()

    second = socketio.test_client(app, auth={"token": admin_token})
    events = second.get_received()

    usernames = [user["username"] for user in events[0]["args"][0]]
    assert usernames == ["admin"]

    first.disconnect()
    second.disconnect()


def test_chat_message_is_broadcast_to_everyone(app, admin_token, analyst_token):
    from app.extensions import socketio

    admin_socket = socketio.test_client(app, auth={"token": admin_token})
    analyst_socket = socketio.test_client(app, auth={"token": analyst_token})
    admin_socket.get_received()
    analyst_socket.get_received()

    admin_socket.emit("chat_message", {"content": "大家好，我是管理员"})

    analyst_events = [e for e in analyst_socket.get_received() if e["name"] == "chat_message"]
    assert len(analyst_events) == 1
    payload = analyst_events[0]["args"][0]
    assert payload["content"] == "大家好，我是管理员"
    assert payload["username"] == "admin"
    assert payload["displayName"] == "系统管理员"

    admin_socket.disconnect()
    analyst_socket.disconnect()


def test_socket_message_is_persisted(app, client, admin_token, admin_headers, analyst_token):
    from app.extensions import socketio

    admin_socket = socketio.test_client(app, auth={"token": admin_token})
    admin_socket.emit("chat_message", {"content": "落库验证"})
    admin_socket.disconnect()

    contents = [m["content"] for m in client.get("/api/chat/messages", headers=admin_headers).get_json()["data"]]
    assert "落库验证" in contents
