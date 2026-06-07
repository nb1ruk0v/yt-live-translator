from dataclasses import dataclass
from pathlib import Path

import ffmpeg

from segment import Segment

ATEMPO_MAX = 1.7  # hard atempo ceiling; pitch-preserving speedup, last resort in the cascade
AUDIO_SOFT = 1.25  # soft atempo cap tried before slowing video
VIDEO_MIN = 0.5  # slowest the window's video is allowed to play


@dataclass
class SegmentPlan:
    audio_tempo: float  # atempo factor (>= 1.0)
    video_speed: float  # playback speed of the window's video (<= 1.0 slows it)
    target_dur: float  # wall-clock duration the window occupies in the output
    new_start: float  # absolute start in the rebuilt timeline; set by plan_timeline
    truncated: float  # seconds of audio dropped by the safety atrim


def _plan_segment(a: float, w: float) -> SegmentPlan:
    """Cascade for one window: soft audio speedup → slow video → hard audio → trim."""
    if w <= 0:
        # overlapping/broken timings: no video to slow, let audio overflow
        return SegmentPlan(1.0, 1.0, 0.0, 0.0, 0.0)
    if a <= w:
        return SegmentPlan(1.0, 1.0, w, 0.0, 0.0)

    tempo = min(AUDIO_SOFT, a / w)
    needed = a / tempo
    if needed <= w:
        return SegmentPlan(tempo, 1.0, w, 0.0, 0.0)

    vspeed = w / needed
    if vspeed >= VIDEO_MIN:
        return SegmentPlan(tempo, vspeed, needed, 0.0, 0.0)

    # video pinned at the floor; re-speed audio as hard as allowed, trim the rest
    target = w / VIDEO_MIN
    tempo = min(ATEMPO_MAX, a / target)
    truncated = max(0.0, a / tempo - target)
    return SegmentPlan(tempo, VIDEO_MIN, target, 0.0, truncated)


def plan_timeline(segments: list) -> list[SegmentPlan]:
    """Placeholder — implemented in Task 2."""
    raise NotImplementedError


def merge(video_path: str, segments: list[Segment], suffix: str) -> str:
    input_path = Path(video_path)
    output_path = input_path.with_name(f"{input_path.stem}{suffix}{input_path.suffix}")

    video = ffmpeg.input(video_path).video

    audio_streams = []
    overflow_count = 0
    truncated_total = 0.0
    for i, seg in enumerate(segments):
        stream = ffmpeg.input(seg.audio_path).audio

        is_last = i + 1 >= len(segments)
        effective_window = None if is_last else segments[i + 1].start - seg.start

        if (
            effective_window is not None
            and effective_window > 0
            and seg.audio_duration > effective_window
        ):
            ratio = seg.audio_duration / effective_window
            tempo = min(ATEMPO_MAX, ratio)
            stretched = seg.audio_duration / tempo
            truncated = max(0.0, stretched - effective_window)
            overflow_count += 1
            truncated_total += truncated
            print(
                f"      seg {i:3d}: audio {seg.audio_duration:5.2f}s > "
                f"window {effective_window:5.2f}s, atempo={tempo:.2f}, "
                f"truncated {truncated:.2f}s"
            )
            stream = stream.filter("atempo", tempo)
            stream = stream.filter("atrim", duration=effective_window)

        delay_ms = int(seg.start * 1000)
        stream = stream.filter("adelay", f"{delay_ms}|{delay_ms}")
        audio_streams.append(stream)

    if overflow_count:
        print(
            f"      {overflow_count}/{len(segments)} segments stretched, "
            f"{truncated_total:.2f}s total truncated"
        )

    if audio_streams:
        mixed = ffmpeg.filter(audio_streams, "amix", inputs=len(audio_streams), normalize=0)
        out = ffmpeg.output(video, mixed, str(output_path))
    else:
        out = ffmpeg.output(video, str(output_path))

    out.overwrite_output().run(capture_stdout=True, capture_stderr=True)
    return str(output_path)
