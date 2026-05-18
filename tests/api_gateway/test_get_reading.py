import httpx


def test_get_reading_endpoint(api_client: httpx.Client, completed_reading: dict) -> None:
    response = api_client.get(f"/api/v1/readings/{completed_reading['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == completed_reading["id"]
    assert data["status"] == "completed"
    assert data["corrected_text_key"].endswith("/corrected.md")
    assert data["recording_key"].endswith("/recording.mp3")
