from diarize import _assign_speaker


def test_max_overlap_picks_dominant_speaker():
    intervals = [
        (0.0, 1.0, "SPEAKER_00"),
        (1.0, 5.0, "SPEAKER_01"),
    ]
    # segment 0..4 overlaps SPEAKER_00 by 1s, SPEAKER_01 by 3s
    assert _assign_speaker(0.0, 4.0, intervals) == "SPEAKER_01"


def test_no_overlap_returns_unknown():
    intervals = [
        (0.0, 1.0, "SPEAKER_00"),
        (10.0, 12.0, "SPEAKER_01"),
    ]
    assert _assign_speaker(5.0, 6.0, intervals) == "SPEAKER_UNKNOWN"


def test_partial_overlap_counted_correctly():
    intervals = [
        (0.0, 5.0, "SPEAKER_00"),
        (4.5, 10.0, "SPEAKER_01"),
    ]
    # segment 4..6: overlaps SPEAKER_00 by 1.0, SPEAKER_01 by 1.5
    assert _assign_speaker(4.0, 6.0, intervals) == "SPEAKER_01"


def test_segment_fully_inside_one_interval():
    intervals = [(0.0, 100.0, "SPEAKER_00")]
    assert _assign_speaker(10.0, 20.0, intervals) == "SPEAKER_00"


def test_empty_intervals_returns_unknown():
    assert _assign_speaker(0.0, 1.0, []) == "SPEAKER_UNKNOWN"
