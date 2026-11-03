"""Verify the login form, signed identity, and logout."""

import pytest
from werkzeug.security import check_password_hash

from app import create_app
from app.models import Role

DEMO_CONFIG = {
    "SECRET_KEY": "test-key-only-not-for-deployment",
    "DEMO_LECTURER_PASSWORD": "synthetic-lecturer-password",
    "DEMO_STUDENT_PASSWORD": "synthetic-student-password",
}


@pytest.fixture(scope="module")
def app():
    return create_app(config={**DEMO_CONFIG, "TESTING": True, "SESSION_COOKIE_SECURE": False})


def form_token(client):
    assert client.get("/auth/login").status_code == 200
    with client.session_transaction() as browser_session:
        return browser_session["csrf_token"]


def sign_in(client, username="student", password=DEMO_CONFIG["DEMO_STUDENT_PASSWORD"]):
    return client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
            "csrf_token": form_token(client),
            "role": "lecturer",
            "actor_id": "999",
        },
    )


@pytest.mark.parametrize("role", [Role.LECTURER, Role.STUDENT])
def test_demo_login_resolves_stored_role(app, role):
    password = DEMO_CONFIG[f"DEMO_{role.value.upper()}_PASSWORD"]
    user = app.extensions["repository"].find_user_by_username(role.value)
    assert user.password_hash != password
    assert check_password_hash(user.password_hash, password)

    client = app.test_client()
    old_token = form_token(client)
    response = sign_in(client, role.value, password)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/me")
    assert "HttpOnly" in response.headers["Set-Cookie"]
    assert "SameSite=Lax" in response.headers["Set-Cookie"]

    identity = client.get("/auth/me")
    assert identity.get_json() == {"id": user.id, "username": user.username, "role": role.value}
    assert identity.headers["Cache-Control"] == "no-store"
    with client.session_transaction() as browser_session:
        assert browser_session["csrf_token"] != old_token
        assert browser_session["user_id"] == user.id
        assert browser_session.permanent

    client.set_cookie("session", "tampered-cookie")
    assert client.get("/auth/me").status_code == 401


@pytest.mark.parametrize(
    "username,password", [("student", "wrong"), ("missing", "wrong"), ("", "")]
)
def test_invalid_credentials_are_generic(app, username, password):
    client = app.test_client()
    response = sign_in(client, username, password)

    assert response.status_code == 401
    assert b"Invalid username or password" in response.data
    assert client.get("/auth/me").status_code == 401


@pytest.mark.parametrize("value", [None, "wrong", "\u00e9"])
def test_login_requires_valid_csrf_token(app, value):
    client = app.test_client()
    form_token(client)
    data = {"username": "student", "password": DEMO_CONFIG["DEMO_STUDENT_PASSWORD"]}
    if value is not None:
        data["csrf_token"] = value

    assert client.post("/auth/login", data=data).status_code == 400
    assert client.get("/auth/me").status_code == 401


def test_logout_requires_post_and_csrf(app):
    client = app.test_client()
    assert sign_in(client).status_code == 302
    assert client.get("/auth/logout").status_code == 405
    assert client.post("/auth/logout").status_code == 400
    assert client.get("/auth/me").status_code == 200

    response = client.post("/auth/logout", data={"csrf_token": form_token(client)})
    assert response.status_code == 302
    assert client.get("/auth/me").status_code == 401


def test_stale_session_is_cleared(app):
    client = app.test_client()
    with client.session_transaction() as browser_session:
        browser_session["user_id"] = 999

    assert client.get("/auth/me").status_code == 401
    with client.session_transaction() as browser_session:
        assert "user_id" not in browser_session


def test_health_remains_public_without_login_configuration():
    app = create_app(config=dict.fromkeys(DEMO_CONFIG))
    client = app.test_client()

    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 200
    assert client.get("/auth/login").status_code == 503


def test_partial_demo_configuration_is_rejected():
    with pytest.raises(ValueError, match="both demo passwords"):
        create_app(config={**DEMO_CONFIG, "DEMO_STUDENT_PASSWORD": None})
