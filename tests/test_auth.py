def test_register_login_and_me(client):
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Owner",
            "email": "owner@example.com",
            "password": "strong-password",
            "pharmacy_name": "Example Pharmacy",
        },
    )
    assert registration.status_code == 201

    login = client.post(
        "/api/v1/auth/login",
        data={"username": "owner@example.com", "password": "strong-password"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "owner@example.com"
