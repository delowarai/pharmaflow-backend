def test_docs_are_available(client):
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    assert "/api/v1/auth/login" in response.json()["paths"]
