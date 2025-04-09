from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"name": "TestUser", "email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
