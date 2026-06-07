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


def plan_timeline(segments: list[Segment], video_total: float) -> list[SegmentPlan]:
    """Per-segment fit plan with cumulative output offsets.

    `cursor` is the running position in the rebuilt timeline; it is monotonically
    non-decreasing because `_plan_segment` never returns target_dur < w (windows
    expand or stay the same, never shrink). `w` is the segment's *original* video
    span, which is what gets stretched — so it is measured off `seg.start`, not `cursor`.
    """
    plans: list[SegmentPlan] = []
    if not segments:
        return plans
    cursor = segments[0].start  # preroll plays at normal speed before the first segment
    for i, seg in enumerate(segments):
        w_end = segments[i + 1].start if i + 1 < len(segments) else video_total
        w = w_end - seg.start  # original window span (gets stretched, not the cursor)
        plan = _plan_segment(seg.audio_duration, w)
        plan.new_start = cursor
        cursor += plan.target_dur
        plans.append(plan)
    return plans


def merge(video_path: str, segments: list[Segment], suffix: str) -> str:
    input_path = Path(video_path)
    output_path = input_path.with_name(f"{input_path.stem}{suffix}{input_path.suffix}")

    if not segments:
        vinput = ffmpeg.input(video_path)
        ffmpeg.output(vinput.video, str(output_path)).overwrite_output().run(
            capture_stdout=True, capture_stderr=True
        )
        return str(output_path)

    video_total = float(ffmpeg.probe(video_path)["format"]["duration"])
    vinput = ffmpeg.input(video_path)
    plans = plan_timeline(segments, video_total)

    video_pieces = []
    if segments[0].start > 0:
        pre = vinput.video.filter("trim", start=0, end=segments[0].start)
        pre = pre.filter("setpts", "PTS-STARTPTS")
        video_pieces.append(pre)

    audio_streams = []
    overflow_count = 0
    truncated_total = 0.0
    extended_total = 0.0
    for i, (seg, plan) in enumerate(zip(segments, plans)):
        # window span mirrors plan_timeline; merge needs raw w to compute the setpts factor
        w_end = segments[i + 1].start if i + 1 < len(segments) else video_total
        w = w_end - seg.start

        if plan.target_dur > 0 and w > 0:
            piece = vinput.video.filter("trim", start=seg.start, end=seg.start + w)
            if plan.target_dur > w:
                factor = plan.target_dur / w
                piece = piece.filter("setpts", f"(PTS-STARTPTS)*{factor:.6f}")
                extended_total += plan.target_dur - w
            else:
                piece = piece.filter("setpts", "PTS-STARTPTS")
            video_pieces.append(piece)

        stream = ffmpeg.input(seg.audio_path).audio
        if plan.audio_tempo > 1.0:
            stream = stream.filter("atempo", plan.audio_tempo)
        if plan.truncated > 0:
            stream = stream.filter("atrim", duration=plan.target_dur)
            overflow_count += 1
            truncated_total += plan.truncated
        if plan.video_speed < 1.0 or plan.truncated > 0:
            trunc_note = f", truncated {plan.truncated:.2f}s" if plan.truncated > 0 else ""
            print(
                f"      seg {i:3d}: audio {seg.audio_duration:5.2f}s, "
                f"vspeed={plan.video_speed:.2f}, atempo={plan.audio_tempo:.2f}{trunc_note}"
            )
        delay_ms = int(plan.new_start * 1000)
        stream = stream.filter("adelay", f"{delay_ms}|{delay_ms}")
        audio_streams.append(stream)

    if extended_total or truncated_total:
        print(
            f"      video extended +{extended_total:.2f}s, "
            f"{overflow_count} segments truncated {truncated_total:.2f}s total"
        )

    if not video_pieces:
        video_out = vinput.video
    elif len(video_pieces) == 1:
        video_out = video_pieces[0]
    else:
        video_out = ffmpeg.concat(*video_pieces, v=1, a=0)

    mixed = ffmpeg.filter(audio_streams, "amix", inputs=len(audio_streams), normalize=0)
    out = ffmpeg.output(video_out, mixed, str(output_path))
    out.overwrite_output().run(capture_stdout=True, capture_stderr=True)
    return str(output_path)
