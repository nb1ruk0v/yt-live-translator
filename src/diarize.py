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
