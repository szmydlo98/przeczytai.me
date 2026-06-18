import json
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.config import Settings


EDGE_TTS_VENDOR = "edge-tts"
OPENAI_TTS_VENDOR = "openai"
DEFAULT_TTS_VENDOR = EDGE_TTS_VENDOR

TTS_VENDOR = DEFAULT_TTS_VENDOR
EDGE_TTS_VOICES = {
    "Zofia": "pl-PL-ZofiaNeural",
    "Marek": "pl-PL-MarekNeural",
    "Ava": "en-US-AvaMultilingualNeural",
    "Andrew": "en-US-AndrewMultilingualNeural",
    "Brian": "en-US-BrianMultilingualNeural",
    "Emma": "en-US-EmmaMultilingualNeural",
}
EDGE_TTS_VOICE = EDGE_TTS_VOICES["Zofia"]
TTS_VOICES = EDGE_TTS_VOICES
TTS_VOICE = EDGE_TTS_VOICE

OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_TTS_INPUT_MAX_CHARS = 4096
OPENAI_TTS_VOICE = "alloy"
OPENAI_TTS_VOICES = {
    "alloy": "alloy",
    "ash": "ash",
    "ballad": "ballad",
    "coral": "coral",
    "echo": "echo",
    "fable": "fable",
    "marin": "marin",
    "nova": "nova",
    "onyx": "onyx",
    "sage": "sage",
    "shimmer": "shimmer",
    "verse": "verse",
    "cedar": "cedar",
}


class TtsError(Exception):
    pass


class UnsupportedTtsVendorError(TtsError):
    def __init__(self, vendor: str) -> None:
        self.vendor = vendor
        super().__init__(f"Unsupported TTS vendor: {vendor}")


class TtsInputTooLargeError(TtsError):
    def __init__(self, vendor: str, max_chars: int) -> None:
        self.vendor = vendor
        self.max_chars = max_chars
        super().__init__(f"{vendor} TTS input must be {max_chars} characters or fewer")


class TtsProviderUnavailableError(TtsError):
    def __init__(self, vendor: str) -> None:
        self.vendor = vendor
        super().__init__(f"{vendor} TTS is not configured")


class TtsConfigurationError(TtsError):
    pass


@dataclass(frozen=True)
class TtsSelection:
    vendor: str
    voice: str


Synthesizer = Callable[[str, str, TtsSelection, Settings | None], Awaitable[None]]


@dataclass(frozen=True)
class TtsProvider:
    vendor: str
    default_voice: str
    voices: Mapping[str, str]
    synthesizer: Synthesizer
    model: str | None = None
    output_format: str = "mp3"
    output_extension: str = "mp3"
    content_type: str = "audio/mpeg"
    max_input_chars: int | None = None

    def resolve_voice(self, voice: str | None) -> str:
        if not voice:
            return self.default_voice
        normalized_voice = voice.strip()
        if normalized_voice in self.voices:
            return self.voices[normalized_voice]
        if normalized_voice in self.voices.values():
            return normalized_voice
        return self.default_voice


def resolve_tts_voice(voice: str | None) -> str:
    return resolve_tts_selection(None, voice).voice


async def _synthesize_edge_tts_to_file(
    text: str,
    output_path: str,
    selection: TtsSelection,
    settings: Settings | None,
) -> None:
    del settings
    import edge_tts

    communicate = edge_tts.Communicate(text, selection.voice)
    await communicate.save(output_path)


async def _synthesize_openai_to_file(
    text: str,
    output_path: str,
    selection: TtsSelection,
    settings: Settings | None,
) -> None:
    from openai import AsyncOpenAI

    api_key = get_openai_api_key(settings)
    if not api_key:
        raise TtsProviderUnavailableError(OPENAI_TTS_VENDOR)

    async with AsyncOpenAI(api_key=api_key) as client:
        async with client.audio.speech.with_streaming_response.create(
            model=OPENAI_TTS_MODEL,
            voice=selection.voice,
            input=text,
            response_format=get_tts_provider(selection.vendor).output_format,
        ) as response:
            Path(output_path).write_bytes(await response.read())


# Add another vendor here; the API, repository, and processor stay on the same path.
TTS_PROVIDERS: dict[str, TtsProvider] = {
    EDGE_TTS_VENDOR: TtsProvider(
        vendor=EDGE_TTS_VENDOR,
        default_voice=EDGE_TTS_VOICE,
        voices=EDGE_TTS_VOICES,
        synthesizer=_synthesize_edge_tts_to_file,
    ),
    OPENAI_TTS_VENDOR: TtsProvider(
        vendor=OPENAI_TTS_VENDOR,
        default_voice=OPENAI_TTS_VOICE,
        voices=OPENAI_TTS_VOICES,
        synthesizer=_synthesize_openai_to_file,
        model=OPENAI_TTS_MODEL,
        max_input_chars=OPENAI_TTS_INPUT_MAX_CHARS,
    ),
}


def get_tts_provider(vendor: str | None) -> TtsProvider:
    normalized_vendor = (vendor or DEFAULT_TTS_VENDOR).strip().lower() or DEFAULT_TTS_VENDOR
    try:
        return TTS_PROVIDERS[normalized_vendor]
    except KeyError as exc:
        raise UnsupportedTtsVendorError(normalized_vendor) from exc


def resolve_tts_selection(vendor: str | None, voice: str | None) -> TtsSelection:
    provider = get_tts_provider(vendor)
    return TtsSelection(
        vendor=provider.vendor,
        voice=provider.resolve_voice(voice),
    )


def _openai_tts_configured(settings: Settings | None) -> bool:
    if not settings:
        return False
    if settings.openai_tts_enabled is not None:
        return settings.openai_tts_enabled
    return bool(
        (settings.openai_api_key and settings.openai_api_key.strip())
        or (settings.openai_api_key_secret_arn and settings.openai_api_key_secret_arn.strip())
    )


def ensure_tts_provider_available(selection: TtsSelection, settings: Settings | None) -> None:
    if selection.vendor == OPENAI_TTS_VENDOR and not _openai_tts_configured(settings):
        raise TtsProviderUnavailableError(selection.vendor)


def tts_metadata(selection: TtsSelection) -> dict[str, object]:
    provider = get_tts_provider(selection.vendor)
    metadata: dict[str, object] = {
        "processor": provider.vendor,
        "voice": selection.voice,
    }
    if provider.model:
        metadata["model"] = provider.model
    return metadata


def validate_tts_input(text: str, selection: TtsSelection) -> None:
    provider = get_tts_provider(selection.vendor)
    if provider.max_input_chars is None:
        return
    if len(text) > provider.max_input_chars:
        raise TtsInputTooLargeError(selection.vendor, provider.max_input_chars)


@lru_cache
def _get_secret_string(secret_id: str) -> str:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    try:
        response = boto3.client("secretsmanager").get_secret_value(SecretId=secret_id)
    except (BotoCoreError, ClientError) as exc:
        raise TtsConfigurationError("Failed to load OpenAI API key secret") from exc

    secret_string = response.get("SecretString")
    if secret_string:
        return str(secret_string)

    secret_binary = response.get("SecretBinary")
    if isinstance(secret_binary, bytes):
        return secret_binary.decode()
    if isinstance(secret_binary, str):
        return secret_binary
    raise TtsConfigurationError("OpenAI API key secret is empty")


def _extract_openai_api_key(secret: str) -> str:
    secret = secret.strip()
    if not secret:
        return ""
    try:
        payload = json.loads(secret)
    except json.JSONDecodeError:
        return secret
    if isinstance(payload, str):
        return payload.strip()
    if not isinstance(payload, dict):
        return ""
    for key in ("OPENAI_API_KEY", "openai_api_key", "api_key"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def get_openai_api_key(settings: Settings | None) -> str | None:
    if settings and settings.openai_api_key and settings.openai_api_key.strip():
        return settings.openai_api_key.strip()
    if settings and settings.openai_api_key_secret_arn:
        secret_id = settings.openai_api_key_secret_arn.strip()
        api_key = _extract_openai_api_key(_get_secret_string(secret_id)) if secret_id else ""
        if api_key:
            return api_key
    return None


async def synthesize_to_file(
    text: str,
    output_path: str,
    selection: TtsSelection | str | None = None,
    settings: Settings | None = None,
) -> None:
    resolved_selection = (
        selection if isinstance(selection, TtsSelection) else resolve_tts_selection(None, selection)
    )
    validate_tts_input(text, resolved_selection)
    provider = get_tts_provider(resolved_selection.vendor)
    await provider.synthesizer(text, output_path, resolved_selection, settings)
