
def test_register_user(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "thomas123",
        "confirm_password": "thomas123"
    }
    res = client.post("/auth/register", json=payload)

    assert res.status_code == 201
    data = res.get_json()
    assert data["message"] == "User created successfully"

def test_login_user(client):
    client.post("/auth/register", json={
        "username": "john",
        "email": "john@test.com",
        "password": "john12345",
        "confirm_password": "john12345"
        })

    res = client.post("/auth/login", json={
        "username": "john",
        "password": "john12345"
    })

    assert res.status_code == 200
    data = res.get_json()

    assert "access_token" in data
    assert data["message"] == "Login successful"


