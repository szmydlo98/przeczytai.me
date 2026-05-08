from app.processing import handler


def test_processing_placeholder_returns_ok() -> None:
    event = {"textcording_id": "job-1", "owner_user_id": "user-1"}

    assert handler(event, None) == {"status": "ok"}
