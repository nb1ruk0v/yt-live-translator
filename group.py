from dataclasses import replace
from segment import Segment


def group_segments(
    segments: list[Segment],
    gap_threshold: float,
    max_duration: float = 12.0,
) -> list[Segment]:
    if not segments:
        return []

    merged: list[Segment] = [replace(segments[0])]
    for seg in segments[1:]:
        prev = merged[-1]
        combined_duration = seg.end - prev.start
        can_merge = (
            seg.start - prev.end < gap_threshold
            and combined_duration <= max_duration
        )
        if can_merge:
            prev.end = seg.end
            prev.original = f"{prev.original} {seg.original}".strip()
        else:
            merged.append(replace(seg))
    return merged
