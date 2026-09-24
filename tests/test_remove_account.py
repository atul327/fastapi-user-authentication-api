from fastapi.testclient import TestClient
from main import app

from unittest.mock import MagicMock, patch

client = TestClient(app)

def test_remove_acc():
    fake_cursor = MagicMock()

    fake_cursor.fetchone.return_value = {
        "email": "atul@gmail.com"
    }

    fake_connection = MagicMock()
    fake_connection.cursor.return_value = fake_cursor

    with patch("main.get_connection", return_value = fake_connection):
        response = client.request(
            "DELETE",
            "/remove_acc",
            json={
                "email": "atul@gmail.com"
            }
        )

    assert response.status_code == 200
    assert response.json()== {
        'message' : 'Account deleted'
    }