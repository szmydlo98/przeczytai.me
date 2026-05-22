import asyncio
import logging
from pathlib import Path
from typing import Any

from app.config import Settings, get_settings
from app.repositories.readings import ReadingRepository
from app.storage import FileStorage
from app.tts import TTS_VENDOR, TTS_VOICE, synthesize_to_file


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def process_reading(
    event: dict[str, Any],
    settings: Settings | None = None,
    storage: FileStorage | None = None,
    repo: ReadingRepository | None = None,
    synthesize=synthesize_to_file,
) -> dict[str, str]:
    settings = settings or get_settings()
    storage = storage or FileStorage(settings.files_bucket_name)
    repo = repo or ReadingRepository(settings.readings_table_name, None)

    reading_id = str(event["reading_id"])
    owner_user_id = str(event["owner_user_id"])
    original_text_key = str(event["original_text_key"])

    original_text = storage.get_text(original_text_key)
    corrected_text_key = storage.corrected_text_key(owner_user_id, reading_id)
    recording_key = storage.recording_key(owner_user_id, reading_id, "mp3")
    recording_path = Path("/tmp") / f"{reading_id}.mp3"

    logger.info(
        "processing reading",
        extra={
            "reading_id": reading_id,
            "owner_user_id": owner_user_id,
            "voice": TTS_VOICE,
        },
    )

    storage.put_text(corrected_text_key, original_text, "text/markdown; charset=utf-8")
    await synthesize(original_text, str(recording_path))
    storage.put_bytes(recording_key, recording_path.read_bytes(), "audio/mpeg")
    recording_path.unlink(missing_ok=True)

    repo.mark_completed(
        owner_user_id,
        reading_id,
        corrected_text_key,
        recording_key,
        {
            "processor": TTS_VENDOR,
            "voice": TTS_VOICE,
        },
    )
    return {"status": "completed"}


def handler(event: dict[str, Any], _context: Any) -> dict[str, str]:
    return asyncio.run(process_reading(event))
