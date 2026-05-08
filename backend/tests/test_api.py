import asyncio

from fastapi.testclient import TestClient
from starlette.requests import Request

from app.auth import CurrentUser, get_current_user
from app.config import Settings, get_settings
from app.main import app
from app.repositories.textcordings import ProcessingStartError
from app.routes.textcordings import get_textcording_repository


NOW = "2026-05-04T12:00:00Z"


class FakeRepo:
    def __init__(self) -> None:
        self.items: dict[tuple[str, str], dict] = {}
        self.deleted: list[tuple[str, str]] = []

    def create(
        self,
        owner_user_id: str,
        original_text: str,
        vendor: str | None,
        voice: str | None,
    ) -> dict:
        textcording_id = f"id-{len(self.items) + 1}"
        item = {
            "textcording_id": textcording_id,
            "owner_user_id": owner_user_id,
            "original_text": original_text,
            "read_text": None,
            "recording": None,
            "vendor": vendor,
            "voice": voice,
            "status": "processing",
            "metadata": {},
            "char_count": len(original_text),
            "created_at": NOW,
            "updated_at": NOW,
        }
        self.items[(owner_user_id, textcording_id)] = item
        return item

    def list(
        self, owner_user_id: str, limit: int, cursor: str | None
    ) -> tuple[list[dict], str | None]:
        del cursor
        items = [item for (user_id, _), item in self.items.items() if user_id == owner_user_id]
        return items[:limit], None

    def get(self, owner_user_id: str, textcording_id: str) -> dict | None:
        return self.items.get((owner_user_id, textcording_id))

    def delete(self, owner_user_id: str, textcording_id: str) -> None:
        self.deleted.append((owner_user_id, textcording_id))
        self.items.pop((owner_user_id, textcording_id), None)


class FailingProcessingRepo(FakeRepo):
    def create(
        self,
        owner_user_id: str,
        original_text: str,
        vendor: str | None,
        voice: str | None,
    ) -> dict:
        del owner_user_id, original_text, vendor, voice
        raise ProcessingStartError


def client(repo: FakeRepo | None = None, auth: bool = True) -> tuple[TestClient, FakeRepo]:
    app.dependency_overrides.clear()
    repo = repo or FakeRepo()
    app.dependency_overrides[get_settings] = lambda: Settings(max_text_chars=10)
    app.dependency_overrides[get_textcording_repository] = lambda: repo
    if auth:
        app.dependency_overrides[get_current_user] = lambda: CurrentUser("user_1")
    return TestClient(app), repo


def test_health() -> None:
    test_client, _ = client()
    assert test_client.get("/api/v1/health").json() == {"status": "ok"}


def test_create_rejects_empty_original_text() -> None:
    test_client, _ = client()
    response = test_client.post("/api/v1/textcordings", json={"original_text": "   "})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_create_rejects_large_original_text() -> None:
    test_client, _ = client()
    response = test_client.post("/api/v1/textcordings", json={"original_text": "x" * 11})
    assert response.status_code == 413
    assert response.json()["error"]["code"] == "payload_too_large"


def test_create_and_get_textcording() -> None:
    test_client, _ = client()
    created = test_client.post(
        "/api/v1/textcordings",
        json={"original_text": "hello", "vendor": "aws-polly", "voice": "Ola"},
    ).json()

    assert created["original_text"] == "hello"
    assert created["read_text"] is None
    assert created["recording"] is None
    assert created["vendor"] == "aws-polly"
    assert created["voice"] == "Ola"
    assert created["status"] == "processing"
    assert created["char_count"] == 5

    detail = test_client.get(f"/api/v1/textcordings/{created['id']}").json()
    assert detail["original_text"] == "hello"


def test_create_returns_500_when_processing_start_fails() -> None:
    test_client, _ = client(FailingProcessingRepo())

    response = test_client.post("/api/v1/textcordings", json={"original_text": "hello"})

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "processing_start_failed"


def test_list_is_user_scoped() -> None:
    repo = FakeRepo()
    repo.create("user_1", "mine", None, None)
    repo.create("user_2", "other", None, None)
    test_client, _ = client(repo)

    response = test_client.get("/api/v1/textcordings").json()
    assert [item["original_text"] for item in response["items"]] == ["mine"]


def test_get_missing_returns_404() -> None:
    test_client, _ = client()
    response = test_client.get("/api/v1/textcordings/missing")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_get_other_user_item_returns_404() -> None:
    repo = FakeRepo()
    item = repo.create("user_2", "other", None, None)
    test_client, _ = client(repo)

    response = test_client.get(f"/api/v1/textcordings/{item['textcording_id']}")
    assert response.status_code == 404


def test_delete_textcording() -> None:
    repo = FakeRepo()
    item = repo.create("user_1", "hello", None, None)
    test_client, _ = client(repo)

    response = test_client.delete(f"/api/v1/textcordings/{item['textcording_id']}")
    assert response.status_code == 204
    assert repo.get("user_1", item["textcording_id"]) is None


def test_missing_jwt_returns_401() -> None:
    test_client, _ = client(auth=False)
    response = test_client.get("/api/v1/textcordings")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


def test_auth_reads_api_gateway_jwt_claims() -> None:
    request = Request(
        {
            "type": "http",
            "headers": [],
            "aws.event": {
                "requestContext": {
                    "authorizer": {
                        "jwt": {
                            "claims": {
                                "sub": "user_gateway",
                            }
                        }
                    }
                }
            },
        }
    )

    user = asyncio.run(get_current_user(request))
    assert user.user_id == "user_gateway"
