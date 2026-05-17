import logging
from typing import Any


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event: dict[str, Any], context: Any) -> dict[str, str]:
    del context
    logger.info(
        "hello world",
        extra={
            "reading_id": event.get("reading_id"),
            "owner_user_id": event.get("owner_user_id"),
        },
    )
    return {"status": "ok"}
