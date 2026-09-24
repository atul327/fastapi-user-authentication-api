from fastapi.testclient import TestClient
from main import app

from unittest.mock import MagicMock, patch

client = TestClient(app)

def test_register_success():
    fake_cursor = MagicMock()

    fake_cursor.fetchone.return_value = None 

    fake_connection = MagicMock()
    fake_connection.cursor.return_value = fake_cursor

    with patch("main.get_connection", return_value= fake_connection):
        with patch("main.pwd_context.hash", return_value = "fake_hashed_pass"):
            response = client.post(
                "/register",
                json = {
                    "email": "atul@gmail.com",
                    "year": 2005,
                    "password": "atul@123",
                    "conf_password": "atul@123"
                }
            )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Registration Successfull!"
    }

def test_register_wrong_password():
    
    response = client.post(
            "/register",
            json = {
                "email": "atul@gmail.com",
                "year": 2005,
                "password": "atul@123",
                "conf_password": "atul@444"
            }
        )
    
    assert response.status_code == 422

def test_email_already_exixts():
    fake_cursor = MagicMock()

    fake_cursor.fetchone.return_value = {
        "email": "atul@gmail.com",
        "year": 2005,
        "password": "fake_hash_pass"
    }

    fake_connection = MagicMock()

    fake_connection.cursor.return_value = fake_cursor

    with patch("main.get_connection", return_value = fake_connection):
        response = client.post(
            "/register",
            json={
                "email": "atul@gmail.com",
                "year": 2005,
                "password": "atul@123",
                "conf_password": "atul@123"
            }
        )

    assert response.status_code == 500