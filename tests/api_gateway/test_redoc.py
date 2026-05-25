import httpx


def test_redoc_endpoint(api_client: httpx.Client) -> None:
    response = api_client.get("/redoc")

    assert response.status_code == 200
    assert "redoc" in response.text.lower()
