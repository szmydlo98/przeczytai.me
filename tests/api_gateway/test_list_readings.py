import httpx


def test_list_readings_endpoint(api_client: httpx.Client, completed_reading: dict) -> None:
    response = api_client.get("/api/v1/readings")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
    assert any(item["id"] == completed_reading["id"] for item in data["items"])
