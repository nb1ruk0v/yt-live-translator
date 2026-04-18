from segment import Segment
from group import group_segments


def test_group_empty():
    assert group_segments([], gap_threshold=0.3) == []


def test_group_single_unchanged():
    segs = [Segment(start=0.0, end=1.0, original="Hello")]
    result = group_segments(segs, gap_threshold=0.3)
    assert len(result) == 1
    assert result[0].original == "Hello"
    assert result[0].end == 1.0


def test_group_merges_small_gap():
    segs = [
        Segment(start=0.0, end=1.0, original="Hello"),
        Segment(start=1.2, end=2.0, original="world"),
    ]
    result = group_segments(segs, gap_threshold=0.3)
    assert len(result) == 1
    assert result[0].start == 0.0
    assert result[0].end == 2.0
    assert result[0].original == "Hello world"


def test_group_keeps_large_gap():
    segs = [
        Segment(start=0.0, end=1.0, original="Hello"),
        Segment(start=2.0, end=3.0, original="world"),
    ]
    result = group_segments(segs, gap_threshold=0.3)
    assert len(result) == 2
    assert result[0].original == "Hello"
    assert result[1].original == "world"


def test_group_chain_merges():
    segs = [
        Segment(start=0.0, end=1.0, original="A"),
        Segment(start=1.1, end=2.0, original="B"),
        Segment(start=2.15, end=3.0, original="C"),
    ]
    result = group_segments(segs, gap_threshold=0.3)
    assert len(result) == 1
    assert result[0].original == "A B C"
    assert result[0].end == 3.0


def test_group_respects_boundary():
    segs = [
        Segment(start=0.0, end=1.0, original="A"),
        Segment(start=1.1, end=2.0, original="B"),
        Segment(start=5.0, end=6.0, original="C"),
        Segment(start=6.1, end=7.0, original="D"),
    ]
    result = group_segments(segs, gap_threshold=0.3)
    assert len(result) == 2
    assert result[0].original == "A B"
    assert result[0].end == 2.0
    assert result[1].original == "C D"
    assert result[1].end == 7.0


def test_group_respects_max_duration():
    segs = [
        Segment(start=0.0, end=3.0, original="A"),
        Segment(start=3.1, end=6.0, original="B"),
        Segment(start=6.1, end=9.0, original="C"),
    ]
    # max_duration=5.0 — A+B=6s exceeds, so no merge
    result = group_segments(segs, gap_threshold=0.3, max_duration=5.0)
    assert len(result) == 3


def test_group_partial_chain_by_max_duration():
    segs = [
        Segment(start=0.0, end=2.0, original="A"),
        Segment(start=2.1, end=4.0, original="B"),
        Segment(start=4.1, end=6.0, original="C"),
    ]
    # A+B=4s OK, A+B+C=6s exceeds 5s
    result = group_segments(segs, gap_threshold=0.3, max_duration=5.0)
    assert len(result) == 2
    assert result[0].original == "A B"
    assert result[1].original == "C"


def test_group_does_not_mutate_input():
    segs = [
        Segment(start=0.0, end=1.0, original="A"),
        Segment(start=1.1, end=2.0, original="B"),
    ]
    original_end = segs[0].end
    original_text = segs[0].original
    group_segments(segs, gap_threshold=0.3)
    assert segs[0].end == original_end
    assert segs[0].original == original_text
