from app.errors import ApiException
from app.repositories.readings import ProcessingStartError, ReadingRepository
from app.storage import FileStorage, StorageError
from app.tts import TTS_VENDOR, TTS_VOICE


def create_reading_for_user(
    *,
    owner_user_id: str,
    original_text: str,
    max_text_chars: int,
    repo: ReadingRepository,
    storage: FileStorage,
) -> dict:
    original_text = original_text.strip()
    if not original_text:
        raise ApiException("validation_error", "Original text must not be empty", 422)
    if len(original_text) > max_text_chars:
        raise ApiException("payload_too_large", "Original text is too large", 413)

    reading_id = repo.next_id()
    original_text_key = storage.original_text_key(owner_user_id, reading_id)
    try:
        storage.put_text(original_text_key, original_text, "text/plain; charset=utf-8")
    except StorageError as exc:
        raise ApiException("storage_error", "Failed to store original text", 500) from exc

    try:
        return repo.create(
            owner_user_id,
            reading_id,
            original_text_key,
            len(original_text),
            TTS_VENDOR,
            TTS_VOICE,
        )
    except ProcessingStartError as exc:
        raise ApiException(
            "processing_start_failed",
            "Failed to start reading processing",
            500,
        ) from exc
