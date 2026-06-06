import httpx


def test_readings_require_bearer_token(public_api_client: httpx.Client) -> None:
    response = public_api_client.get("/api/v1/readings")

    assert response.status_code == 401
