from app.processing import handler


def test_processing_placeholder_returns_ok() -> None:
    """Return ok from the placeholder processing handler."""
    event = {
        "reading_id": "job-1",
        "owner_user_id": "user-1",
        "original_text_key": "users/user-1/readings/job-1/original.txt",
    }

    assert handler(event, None) == {"status": "ok"}
