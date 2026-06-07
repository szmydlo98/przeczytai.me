TTS_VENDOR = "edge-tts"
TTS_VOICES = {
    "Zofia": "pl-PL-ZofiaNeural",
    "Marek": "pl-PL-MarekNeural",
    "Ava": "en-US-AvaMultilingualNeural",
    "Andrew": "en-US-AndrewMultilingualNeural",
    "Brian": "en-US-BrianMultilingualNeural",
    "Emma": "en-US-EmmaMultilingualNeural",
}
SUPPORTED_TTS_VOICES = tuple(TTS_VOICES.values())
TTS_VOICE = TTS_VOICES["Zofia"]


def resolve_tts_voice(voice: str | None) -> str:
    if not voice:
        return TTS_VOICE
    voice = voice.strip()
    if voice in TTS_VOICES:
        return TTS_VOICES[voice]
    if voice in SUPPORTED_TTS_VOICES:
        return voice
    return TTS_VOICE


async def synthesize_to_file(text: str, output_path: str, voice: str | None = None) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, voice or TTS_VOICE)
    await communicate.save(output_path)
