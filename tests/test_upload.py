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

    return fake_connection, fake_cursor

    
def test_upload_file_success(fake_db):
    fake_cursor , fake_connection = fake_db

    fake_cursor.fetchone.return_value = {
        "email": "atul@gmail.com"
    }

    fake_connection.cursor.return_value = fake_cursor

    with patch("main.get_connection", return_value=fake_connection):
        response = client.post(
            "/upload",
            data={
                "email": "atul@gmail.com"
            },
            files={
                "file": ("test.txt", b"Hello Atul", "text/plain")
            }
        )

    assert response.status_code == 200

    assert response.json()["message"] == "File uploaded successfully"

# for checking database connection
def test_check_connection_success(fake_db):
    fake_cursor, fake_connection = fake_db

    with patch("main.get_connection", return_value=fake_connection):
        response = client.get("/check")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Database connected"
    }