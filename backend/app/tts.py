TTS_VENDOR = "edge-tts"
TTS_VOICE = "pl-PL-ZofiaNeural"


async def synthesize_to_file(text: str, output_path: str) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, TTS_VOICE)
    await communicate.save(output_path)
