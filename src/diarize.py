import os
import subprocess

import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook

from segment import Segment


def _assign_speaker(
    seg_start: float,
    seg_end: float,
    intervals: list[tuple[float, float, str]],
) -> str:
    best_speaker = "SPEAKER_UNKNOWN"
    best_overlap = 0.0
    for start, end, speaker in intervals:
        overlap = max(0.0, min(seg_end, end) - max(seg_start, start))
        if overlap > best_overlap:
            best_overlap = overlap
            best_speaker = speaker
    return best_speaker


def _ensure_audio(video_path: str) -> str:
    audio_path = os.path.splitext(video_path)[0] + ".wav"
    if os.path.exists(audio_path):
        return audio_path

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-ac",
            "1",
            "-ar",
            "22050",
            "-vn",
            audio_path,
        ],
        check=True,
        capture_output=True,
    )
    return audio_path


def diarize(video_path: str, segments: list[Segment], config: dict) -> list[Segment]:
    token_env = config.get("hf_token_env", "HUGGINGFACE_TOKEN")
    token = os.environ.get(token_env)
    if not token:
        raise RuntimeError(
            f"{token_env} not set. Add it to .env or export it before running"
            " with diarization enabled."
        )

    audio_path = _ensure_audio(video_path)

    pipeline = Pipeline.from_pretrained(
        config["model"],
        token=token,
    )
    pipeline.to(torch.device(config.get("device", "cpu")))
    with ProgressHook() as hook:
        result = pipeline(audio_path, hook=hook)

    intervals = [
        (turn.start, turn.end, speaker)
        for turn, _, speaker in result.exclusive_speaker_diarization.itertracks(yield_label=True)
    ]

    for seg in segments:
        seg.speaker = _assign_speaker(seg.start, seg.end, intervals)

    return segments
