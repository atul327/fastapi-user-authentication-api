from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from main import app, pwd_context

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Detail": "Hello User!"}


def test_register_invalid_password():
    response = client.post(
        "/register",
        json={
            "email": "atul@gmail.com",
            "year": 2005,
            "password": "123",
            "conf_password": "123"
        }
    )

    assert response.status_code == 422


def test_login_validation():
    response = client.post(
        "/login",
        json={
            "email": "atul@gmail.com"
        }
    )

    assert response.status_code == 422


def test_login_success():
    fake_cursor = MagicMock()

    fake_cursor.fetchone.return_value = {
        "email": "atul@gmail.com",
        "password": "fake_hashed_password"
    }

    fake_connection = MagicMock()
    fake_connection.cursor.return_value = fake_cursor

    with patch("main.get_connection", return_value=fake_connection):
        with patch("main.pwd_context.verify", return_value=True):
            response = client.post(
                "/login",
                json={
                    "email": "atul@gmail.com",
                    "password": "atul@2006"
                }
            )

    assert response.status_code == 200
    assert response.json() == {"message": "Login Successfull!"}