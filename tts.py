import os
import tempfile
import wave
import contextlib
from TTS.api import TTS
from segment import Segment


SPEED_MAX = 1.2


def _wav_duration(path: str) -> float:
    with contextlib.closing(wave.open(path, "rb")) as w:
        frames = w.getnframes()
        rate = w.getframerate()
        return frames / float(rate) if rate else 0.0


def _synth(tts: TTS, config: dict, text: str, out_path: str, speed: float) -> None:
    kwargs: dict = {
        "text": text,
        "language": config["language"],
        "file_path": out_path,
        "speed": speed,
    }
    if config.get("speaker_wav"):
        kwargs["speaker_wav"] = config["speaker_wav"]
    elif config.get("speaker"):
        kwargs["speaker"] = config["speaker"]
    tts.tts_to_file(**kwargs)


def synthesize(segments: list[Segment], config: dict) -> list[Segment]:
    tts = TTS(config["model"])

    for i, seg in enumerate(segments):
        out_path = os.path.join(tempfile.gettempdir(), f"seg_{i:04d}.wav")

        _synth(tts, config, seg.translated, out_path, speed=1.0)
        dur = _wav_duration(out_path)

        window = seg.duration
        if window > 0 and dur > window:
            speed = min(SPEED_MAX, dur / window)
            _synth(tts, config, seg.translated, out_path, speed=speed)
            dur = _wav_duration(out_path)

        seg.audio_path = out_path
        seg.audio_duration = dur

    return segments
