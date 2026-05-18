import httpx

from helpers import create_reading


def test_delete_reading_endpoint(api_client: httpx.Client) -> None:
    created = create_reading(api_client)

    response = api_client.delete(f"/api/v1/readings/{created['id']}")
    assert response.status_code == 204

    get_response = api_client.get(f"/api/v1/readings/{created['id']}")
    assert get_response.status_code == 404
