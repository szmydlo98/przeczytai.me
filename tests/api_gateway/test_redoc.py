import httpx


def test_redoc_endpoint(public_api_client: httpx.Client) -> None:
    response = public_api_client.get("/redoc")

    assert response.status_code == 200
    assert "redoc" in response.text.lower()
