import httpx


def test_readings_require_bearer_token(public_api_client: httpx.Client) -> None:
    response = public_api_client.get("/api/v1/readings")

    assert response.status_code == 401


def test_legacy_api_key_is_not_accepted(public_api_client: httpx.Client) -> None:
    response = public_api_client.get(
        "/api/v1/readings",
        headers={"X-Api-Key": "tatuazyk"},
    )

    assert response.status_code == 401
