import httpx


def test_docs_endpoint(api_client: httpx.Client) -> None:
    response = api_client.get("/docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower()
