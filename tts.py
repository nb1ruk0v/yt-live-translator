import os
import tempfile
from TTS.api import TTS
from segment import Segment


def synthesize(segments: list[Segment], config: dict) -> list[Segment]:
    tts = TTS(config["model"])

    for i, seg in enumerate(segments):
        out_path = os.path.join(tempfile.gettempdir(), f"seg_{i:04d}.wav")

        kwargs: dict = {
            "text": seg.translated,
            "language": config["language"],
            "file_path": out_path,
        }
        if config.get("speaker_wav"):
            kwargs["speaker_wav"] = config["speaker_wav"]

        tts.tts_to_file(**kwargs)
        seg.audio_path = out_path

    return segments
