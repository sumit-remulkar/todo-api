from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_auth_and_crud():
    # signup
    r = client.post("/signup", json={
        "username": "testuser",
        "password": "1234"
    })
    assert r.status_code in [200, 400]  # 400 if already exists

    # login (form data ⚠️)
    r = client.post("/login", data={
        "username": "testuser",
        "password": "1234"
    })
    assert r.status_code == 200
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # create item
    r = client.post("/items/", json={
        "id": 99,
        "title": "test",
        "description": "testing",
        "priority": "low"
    })
    assert r.status_code == 200

    # get items
    r = client.get("/items/")
    assert r.status_code == 200

    # protected route
    r = client.get("/protected", headers=headers)
    assert r.status_code == 200