import httpx


def test_openapi_endpoint(api_client: httpx.Client) -> None:
    response = api_client.get("/openapi.json")

    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "przeczytai.me API"
    assert "/api/v1/readings" in data["paths"]
    assert "/api/v1/readings/{reading_id}/recording" in data["paths"]
