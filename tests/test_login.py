from fastapi.testclient import TestClient
from main import app
from unittest.mock import MagicMock, patch

client = TestClient(app)

def test_login_success():
    fake_cursor = MagicMock()

    fake_cursor.fetchone.return_value = {
        "email": "atul@gmail.com",
        "password": "fake_hashed_pass"
    }

    fake_connection = MagicMock()
    fake_connection.cursor.return_value = fake_cursor

    with patch("main.get_connection", return_value = fake_connection):
        with patch("main.pwd_context.verify", return_value = True):
            response = client.post(
                "/login",
                json={
                    "email": "atul@gmail.com",
                    "password": "atul@123"
                }
            )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Login Successfull!"
    }

def test_email_validation():
    fake_cursor = MagicMock()
    fake_cursor.fetchone.return_value = None

    fake_connection = MagicMock()
    fake_connection.cursor.return_value = fake_cursor

    with patch("main.get_connection", return_value = fake_connection):
        response = client.post(
            "/login",
            json={
                "email": "atul@gmail.com",
                "password": "atul@123"
            }
        )

        assert response.status_code == 500
