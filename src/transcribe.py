import os
import subprocess
import tempfile

from faster_whisper import WhisperModel

from segment import Segment

SENTENCE_END = (".", "!", "?", "…")


def _resegment(
    words: list,
    max_duration: float = 8.0,
    min_duration: float = 1.0,
    pause_threshold: float = 0.4,
) -> list[Segment]:
    if not words:
        return []

    out: list[Segment] = []
    buf: list = []

    for i, w in enumerate(words):
        buf.append(w)
        text = "".join(b.word for b in buf).strip()
        duration = buf[-1].end - buf[0].start
        next_pause = words[i + 1].start - w.end if i + 1 < len(words) else float("inf")

        long_enough = duration >= min_duration
        ends_sentence = text.endswith(SENTENCE_END)
        too_long = duration >= max_duration
        big_pause = next_pause >= pause_threshold

        if (ends_sentence and long_enough) or too_long or (big_pause and long_enough):
            out.append(Segment(start=buf[0].start, end=buf[-1].end, original=text))
            buf = []

    if buf:
        text = "".join(b.word for b in buf).strip()
        out.append(Segment(start=buf[0].start, end=buf[-1].end, original=text))

    return out


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
        segments_gen, _ = model.transcribe(audio_path, language=lang_arg, word_timestamps=True)

        words = [w for seg in segments_gen for w in seg.words]
        return _resegment(words)
    finally:
        if os.path.exists(audio_path):
            os.unlink(audio_path)
