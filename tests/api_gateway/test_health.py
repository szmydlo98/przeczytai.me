import httpx


def test_health_endpoint(public_api_client: httpx.Client) -> None:
    response = public_api_client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
