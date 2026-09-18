def auth_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Owner",
            "email": "owner@example.com",
            "password": "strong-password",
            "pharmacy_name": "Example Pharmacy",
        },
    )
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "owner@example.com", "password": "strong-password"},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_medicine_crud(client):
    headers = auth_headers(client)
    created = client.post(
        "/api/v1/medicines",
        headers=headers,
        json={"brand_name": "Paracetamol", "generic_name": "Acetaminophen"},
    )
    assert created.status_code == 201
    medicine_id = created.json()["id"]

    listed = client.get("/api/v1/medicines", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["brand_name"] == "Paracetamol"

    updated = client.patch(
        f"/api/v1/medicines/{medicine_id}",
        headers=headers,
        json={"reorder_level": 30},
    )
    assert updated.status_code == 200
    assert updated.json()["reorder_level"] == 30

    deleted = client.delete(f"/api/v1/medicines/{medicine_id}", headers=headers)
    assert deleted.status_code == 204
