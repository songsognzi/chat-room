import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402


@pytest.fixture()
def app():
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        }
    )
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, username, password):
    response = client.post("/api/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200, response.get_json()
    return response.get_json()["data"]["token"]


@pytest.fixture()
def admin_token(client):
    return login(client, "admin", "admin123")


@pytest.fixture()
def analyst_token(client):
    return login(client, "analyst", "analyst123")


@pytest.fixture()
def admin_headers(admin_token):
    return {"Authorization": "Bearer " + admin_token}


@pytest.fixture()
def analyst_headers(analyst_token):
    return {"Authorization": "Bearer " + analyst_token}
