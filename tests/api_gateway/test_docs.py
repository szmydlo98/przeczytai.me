import httpx


def test_docs_endpoint(public_api_client: httpx.Client) -> None:
    response = public_api_client.get("/docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower()
