def test_login_logs_require_login(client):
    response = client.get("/api/login-logs")

    assert response.status_code == 401


def test_admin_sees_login_logs_with_expected_fields(client, admin_headers):
    response = client.get("/api/login-logs", headers=admin_headers)

    assert response.status_code == 200
    body = response.get_json()
    assert body["code"] == 0

    logs = body["data"]
    assert len(logs) >= 5
    assert set(logs[0].keys()) == {"id", "username", "ip", "userAgent", "status", "loginAt"}


def test_login_logs_are_sorted_by_time_desc(client, admin_headers):
    logs = client.get("/api/login-logs", headers=admin_headers).get_json()["data"]

    times = [log["loginAt"] for log in logs]
    assert times == sorted(times, reverse=True)


def test_analyst_cannot_read_login_logs(client, analyst_headers):
    response = client.get("/api/login-logs", headers=analyst_headers)

    assert response.status_code == 403
    assert response.get_json()["code"] != 0


def test_successful_login_appends_a_login_log(client, admin_headers):
    before = client.get("/api/login-logs", headers=admin_headers).get_json()["data"]

    client.post("/api/auth/login", json={"username": "analyst", "password": "analyst123"})

    after = client.get("/api/login-logs", headers=admin_headers).get_json()["data"]
    assert len(after) == len(before) + 1

    latest = after[0]
    assert latest["username"] == "analyst"
    assert latest["status"] == "success"
    assert latest["ip"]
