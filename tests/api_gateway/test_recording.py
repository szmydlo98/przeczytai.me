import httpx


def test_recording_endpoint(api_client: httpx.Client, completed_reading: dict) -> None:
    response = api_client.get(
        f"/api/v1/readings/{completed_reading['id']}/recording",
        follow_redirects=False,
    )

    assert response.status_code == 307
    assert "location" in response.headers

    download_response = httpx.get(
        response.headers["location"],
        follow_redirects=True,
        timeout=60.0,
    )
    assert download_response.status_code == 200
    assert download_response.headers["content-type"].startswith("audio/")
    assert len(download_response.content) > 0
