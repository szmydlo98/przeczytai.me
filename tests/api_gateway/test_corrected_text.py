import httpx


def test_corrected_text_endpoint(api_client: httpx.Client, completed_reading: dict) -> None:
    response = api_client.get(f"/api/v1/readings/{completed_reading['id']}/corrected-text.md")

    assert response.status_code == 200
    assert response.text == completed_reading["submitted_text"]
    assert response.headers["content-type"].startswith("text/markdown")
