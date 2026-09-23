from fastapi.testclient import TestClient
from main import app

from unittest.mock import MagicMock, patch

client = TestClient(app)

def test_reset_pass():
    fake_cursor = MagicMock()

    fake_cursor.fetchone.return_value = {
        "email": "atul@gmail.com",
        "year": 2005,
        "password": "old_hashed_password"
    }

    fake_connection = MagicMock()
    fake_connection.cursor.return_value = fake_cursor

    with patch("main.get_connection", return_value = fake_connection):
        with patch("main.pwd_context.hash", return_value = "fake_hashed_password"):
            response = client.put(
                "/reset_password",
                json={
                    "email": "atul@gmail.com",
                    "year": 2005,
                    "new_password": "newpassword123"
                }
            )

    assert response.status_code == 200
    assert response.json() == {
        'message' : 'Passwod is changed'
    }

