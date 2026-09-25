import pytest
from fastapi.testclient import TestClient
from main import app

from unittest.mock import MagicMock, patch

client = TestClient(app)

@pytest.fixture
def fake_db():
    fake_cursor = MagicMock()
    fake_connection = MagicMock()

    fake_connection.cursor.return_value = fake_cursor

    return fake_cursor, fake_connection

def test_remove_acc(fake_db):
    fake_cursor, fake_connection = fake_db

    fake_cursor.fetchone.return_value = {
        "email": "atul@gmail.com"
    }

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