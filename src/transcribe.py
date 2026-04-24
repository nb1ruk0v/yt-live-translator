import os
import subprocess
import tempfile

from faster_whisper import WhisperModel

from segment import Segment


def transcribe(video_path: str, config: dict) -> list[Segment]:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        audio_path = f.name

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-ac",
                "1",
                "-ar",
                "16000",
                "-vn",
                audio_path,
                "-y",
            ],
            check=True,
            capture_output=True,
        )

        model = WhisperModel(
            config["model"],
            device=config["device"],
            compute_type="int8",
        )

        language = config.get("language")
        lang_arg = None if language == "auto" else language
        segments_gen, _ = model.transcribe(audio_path, language=lang_arg)

        return [Segment(start=s.start, end=s.end, original=s.text.strip()) for s in segments_gen]
    finally:
        if os.path.exists(audio_path):
            os.unlink(audio_path)
