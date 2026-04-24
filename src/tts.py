import contextlib
import os
import tempfile
import wave

import numpy as np
import torch

from segment import Segment


def _wav_duration(path: str) -> float:
    with contextlib.closing(wave.open(path, "rb")) as w:
        frames = w.getnframes()
        rate = w.getframerate()
        return frames / float(rate) if rate else 0.0


def _save_wav(path: str, audio: torch.Tensor, sample_rate: int) -> None:
    pcm = (audio.detach().cpu().numpy() * 32767).clip(-32768, 32767).astype(np.int16)
    with contextlib.closing(wave.open(path, "wb")) as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm.tobytes())


def _load_model(config: dict):
    model, _ = torch.hub.load(
        repo_or_dir="snakers4/silero-models",
        model="silero_tts",
        language=config["language"],
        speaker=config["model"],
    )
    return model


def synthesize(segments: list[Segment], config: dict) -> list[Segment]:
    model = _load_model(config)
    speaker = config["speaker"]
    sample_rate = config.get("sample_rate", 48000)

    for i, seg in enumerate(segments):
        out_path = os.path.join(tempfile.gettempdir(), f"seg_{i:04d}.wav")

        audio = model.apply_tts(
            text=seg.translated,
            speaker=speaker,
            sample_rate=sample_rate,
            put_accent=True,
            put_yo=True,
        )
        _save_wav(out_path, audio, sample_rate)

        seg.audio_path = out_path
        seg.audio_duration = _wav_duration(out_path)

    return segments
