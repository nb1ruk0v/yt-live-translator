import os
import subprocess


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
