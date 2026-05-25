import asyncio
from pathlib import Path

from app.config import Settings
from app.processing import process_reading
from app.tts import TTS_VENDOR, TTS_VOICE


class FakeStorage:
    def __init__(self) -> None:
        self.texts = {
            "users/user-1/readings/job-1/original.txt": "Ala ma kota.",
        }
        self.bytes: dict[str, bytes] = {}

    def get_text(self, key: str) -> str:
        return self.texts[key]

    def put_text(self, key: str, content: str, content_type: str) -> None:
        del content_type
        self.texts[key] = content

    def put_bytes(self, key: str, content: bytes, content_type: str) -> None:
        del content_type
        self.bytes[key] = content

    def corrected_text_key(self, owner_user_id: str, reading_id: str) -> str:
        return f"users/{owner_user_id}/readings/{reading_id}/corrected.md"

    def recording_key(self, owner_user_id: str, reading_id: str, extension: str = "mp3") -> str:
        return f"users/{owner_user_id}/readings/{reading_id}/recording.{extension}"


class FakeRepo:
    def __init__(self) -> None:
        self.completed: dict[str, object] | None = None

    def mark_completed(
        self,
        owner_user_id: str,
        reading_id: str,
        corrected_text_key: str,
        recording_key: str,
        metadata: dict[str, object],
    ) -> None:
        self.completed = {
            "owner_user_id": owner_user_id,
            "reading_id": reading_id,
            "corrected_text_key": corrected_text_key,
            "recording_key": recording_key,
            "metadata": metadata,
        }


async def fake_synthesize(text: str, output_path: str) -> None:
    Path(output_path).write_bytes(f"mp3:{text}".encode())


def test_processing_generates_same_text_and_recording() -> None:
    """Generate corrected text, MP3 bytes, and mark the reading completed."""
    event = {
        "reading_id": "job-1",
        "owner_user_id": "user-1",
        "original_text_key": "users/user-1/readings/job-1/original.txt",
    }
    storage = FakeStorage()
    repo = FakeRepo()

    result = asyncio.run(
        process_reading(
            event,
            Settings(readings_table_name="table", files_bucket_name="bucket"),
            storage,
            repo,
            fake_synthesize,
        )
    )

    corrected_text_key = "users/user-1/readings/job-1/corrected.md"
    recording_key = "users/user-1/readings/job-1/recording.mp3"
    assert result == {"status": "completed"}
    assert storage.texts[corrected_text_key] == "Ala ma kota."
    assert storage.bytes[recording_key] == b"mp3:Ala ma kota."
    assert repo.completed == {
        "owner_user_id": "user-1",
        "reading_id": "job-1",
        "corrected_text_key": corrected_text_key,
        "recording_key": recording_key,
        "metadata": {
            "processor": TTS_VENDOR,
            "voice": TTS_VOICE,
        },
    }
