from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from main import app, pwd_context

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Detail": "Hello User!"}

