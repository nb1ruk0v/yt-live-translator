from unittest.mock import MagicMock, patch

from merge import (
    ATEMPO_MAX,
    AUDIO_SOFT,
    VIDEO_MIN,
    _plan_segment,
    merge,
    plan_timeline,
)
from segment import Segment


def make_segments():
    return [
        Segment(
            start=0.0,
            end=2.0,
            original="Hi",
            translated="Привет",
            audio_path="/tmp/seg_0000.wav",
            audio_duration=1.8,
        ),
        Segment(
            start=3.0,
            end=5.0,
            original="Bye",
            translated="Пока",
            audio_path="/tmp/seg_0001.wav",
            audio_duration=1.5,
        ),
    ]


def _setup(mock_ffmpeg):
    """Self-returning filter chain so all filter calls land on one mock."""
    audio_chain = MagicMock()
    audio_chain.filter.return_value = audio_chain
    input_mock = MagicMock()
    input_mock.audio = audio_chain
    mock_ffmpeg.input.return_value = input_mock
    mock_ffmpeg.filter.return_value = MagicMock()
    mock_out = MagicMock()
    mock_ffmpeg.output.return_value = mock_out
    mock_out.overwrite_output.return_value = mock_out
    return audio_chain


def _filter_names(audio_chain):
    return [c.args[0] for c in audio_chain.filter.call_args_list]


@patch("merge.ffmpeg")
def test_merge_returns_output_path_with_suffix(mock_ffmpeg):
    _setup(mock_ffmpeg)
    result = merge("/videos/test.mp4", make_segments(), "_dubbed")
    assert result == "/videos/test_dubbed.mp4"


@patch("merge.ffmpeg")
def test_merge_no_filters_when_audio_fits_window(mock_ffmpeg):
    chain = _setup(mock_ffmpeg)
    merge("/videos/test.mp4", make_segments(), "_dubbed")
    names = _filter_names(chain)
    assert "atrim" not in names
    assert "atempo" not in names


@patch("merge.ffmpeg")
def test_merge_atrim_caps_at_effective_window_not_seg_duration(mock_ffmpeg):
    """Regression guard: cap MUST be next.start-this.start, not this.end-this.start.

    seg.duration = 1.0; effective_window = 2.0 (gap of 1s before next).
    Old code would cap at 1.0, new code caps at 2.0.
    """
    chain = _setup(mock_ffmpeg)
    segs = [
        Segment(
            start=0.0,
            end=1.0,
            original="Hi",
            translated="Привет",
            audio_path="/tmp/x.wav",
            audio_duration=3.0,
        ),
        Segment(
            start=2.0,
            end=3.0,
            original="Bye",
            translated="Пока",
            audio_path="/tmp/y.wav",
            audio_duration=0.5,
        ),
    ]
    merge("/videos/test.mp4", segs, "_dubbed")

    atrim_calls = [c for c in chain.filter.call_args_list if c.args[0] == "atrim"]
    assert len(atrim_calls) == 1
    assert atrim_calls[0].kwargs == {"duration": 2.0}


@patch("merge.ffmpeg")
def test_merge_atempo_ratio_under_cap(mock_ffmpeg):
    chain = _setup(mock_ffmpeg)
    segs = [
        Segment(
            start=0.0,
            end=2.0,
            original="Hi",
            translated="Привет",
            audio_path="/tmp/x.wav",
            audio_duration=2.2,
        ),
        Segment(
            start=2.0,
            end=3.0,
            original="Bye",
            translated="Пока",
            audio_path="/tmp/y.wav",
            audio_duration=0.5,
        ),
    ]
    merge("/videos/test.mp4", segs, "_dubbed")

    atempo_calls = [c for c in chain.filter.call_args_list if c.args[0] == "atempo"]
    assert len(atempo_calls) == 1
    # ratio = 2.2 / 2.0 = 1.1, under cap
    assert abs(atempo_calls[0].args[1] - 1.1) < 1e-6


@patch("merge.ffmpeg")
def test_merge_atempo_clamped_to_upper(mock_ffmpeg):
    """Regression guard: ratio above ATEMPO_MAX is clamped to the cap."""
    chain = _setup(mock_ffmpeg)
    segs = [
        Segment(
            start=0.0,
            end=2.0,
            original="Hi",
            translated="Привет",
            audio_path="/tmp/x.wav",
            audio_duration=10.0,
        ),
        Segment(
            start=2.0,
            end=3.0,
            original="Bye",
            translated="Пока",
            audio_path="/tmp/y.wav",
            audio_duration=0.5,
        ),
    ]
    merge("/videos/test.mp4", segs, "_dubbed")

    atempo_calls = [c for c in chain.filter.call_args_list if c.args[0] == "atempo"]
    assert len(atempo_calls) == 1
    assert abs(atempo_calls[0].args[1] - ATEMPO_MAX) < 1e-6


@patch("merge.ffmpeg")
def test_merge_uses_gap_to_next_segment_as_window(mock_ffmpeg):
    """Audio longer than seg.duration but fits in gap before next → no stretch."""
    chain = _setup(mock_ffmpeg)
    segs = [
        Segment(
            start=0.0,
            end=2.0,
            original="Hi",
            translated="Привет",
            audio_path="/tmp/x.wav",
            audio_duration=2.5,  # > duration=2.0 but < gap=3.0
        ),
        Segment(
            start=3.0,
            end=4.0,
            original="Bye",
            translated="Пока",
            audio_path="/tmp/y.wav",
            audio_duration=0.5,
        ),
    ]
    merge("/videos/test.mp4", segs, "_dubbed")

    names = _filter_names(chain)
    assert "atempo" not in names
    assert "atrim" not in names


@patch("merge.ffmpeg")
def test_merge_last_segment_plays_through_unstretched(mock_ffmpeg):
    """Last segment has no successor — overflow plays out, no truncation."""
    chain = _setup(mock_ffmpeg)
    segs = [
        Segment(
            start=0.0,
            end=2.0,
            original="Hi",
            translated="Привет",
            audio_path="/tmp/x.wav",
            audio_duration=10.0,
        ),
    ]
    merge("/videos/test.mp4", segs, "_dubbed")

    names = _filter_names(chain)
    assert "atempo" not in names
    assert "atrim" not in names


def test_plan_segment_fits_natural():
    # audio shorter than window → no speedup, no slowdown
    p = _plan_segment(a=1.5, w=2.0)
    assert p.audio_tempo == 1.0
    assert p.video_speed == 1.0
    assert p.target_dur == 2.0
    assert p.truncated == 0.0


def test_plan_segment_soft_audio_only():
    # a/w = 1.2 (< AUDIO_SOFT=1.25): soft speedup alone makes it fit, video untouched
    p = _plan_segment(a=2.4, w=2.0)
    assert abs(p.audio_tempo - 1.2) < 1e-6
    assert p.video_speed == 1.0
    assert p.target_dur == 2.0
    assert p.truncated == 0.0


def test_plan_segment_slows_video():
    # a/w = 1.5 > AUDIO_SOFT: audio capped at 1.25, video slowed to fit, no truncation
    p = _plan_segment(a=3.0, w=2.0)
    assert abs(p.audio_tempo - AUDIO_SOFT) < 1e-6
    needed = 3.0 / AUDIO_SOFT  # 2.4
    assert abs(p.target_dur - needed) < 1e-6
    assert abs(p.video_speed - 2.0 / needed) < 1e-6  # 0.8333
    assert p.video_speed >= VIDEO_MIN
    assert p.truncated == 0.0


def test_plan_segment_hits_video_floor_then_hard_audio():
    # huge deficit: video pinned at VIDEO_MIN floor, audio re-sped up to ATEMPO_MAX, tail trimmed
    p = _plan_segment(a=10.0, w=2.0)
    assert p.video_speed == VIDEO_MIN
    target = 2.0 / VIDEO_MIN  # 4.0
    assert abs(p.target_dur - target) < 1e-6
    assert abs(p.audio_tempo - ATEMPO_MAX) < 1e-6
    assert abs(p.truncated - (10.0 / ATEMPO_MAX - target)) < 1e-6  # > 0
    assert p.truncated > 0


def test_plan_segment_nonpositive_window_overflows():
    # w <= 0 (overlapping/broken timings): target 0, no slowdown, audio overflows
    p = _plan_segment(a=3.0, w=0.0)
    assert p.target_dur == 0.0
    assert p.video_speed == 1.0
    assert p.audio_tempo == 1.0


def _seg(start, end, a):
    return Segment(
        start=start,
        end=end,
        original="x",
        translated="ы",
        audio_path="/tmp/x.wav",
        audio_duration=a,
    )


def test_plan_timeline_cumulative_new_start():
    # seg0 window [0,3) w=3 fits a=1.8 → target 3; seg1 last window [3,5) w=2 fits a=1.5 → target 2
    segs = [_seg(0.0, 2.0, 1.8), _seg(3.0, 5.0, 1.5)]
    plans = plan_timeline(segs, video_total=5.0)
    assert plans[0].new_start == 0.0
    assert plans[0].target_dur == 3.0
    assert plans[1].new_start == 3.0  # 0 + target_dur[0]


def test_plan_timeline_slowdown_shifts_later_segments():
    # seg0 [0,2) w=2 with a=3.0: audio capped at AUDIO_SOFT, video slowed (vspeed~0.83),
    # so target = needed = 3/AUDIO_SOFT = 2.4
    # seg1 must start at 2.4, not at its original 2.0
    segs = [_seg(0.0, 2.0, 3.0), _seg(2.0, 4.0, 1.0)]
    plans = plan_timeline(segs, video_total=4.0)
    assert abs(plans[0].target_dur - 3.0 / AUDIO_SOFT) < 1e-6
    assert abs(plans[1].new_start - 3.0 / AUDIO_SOFT) < 1e-6


def test_plan_timeline_last_window_uses_video_total():
    # single segment, window = video_total - start = 4.0; a=3.0 fits → no stretch
    plans = plan_timeline([_seg(1.0, 2.0, 3.0)], video_total=5.0)
    assert plans[0].target_dur == 4.0
    assert plans[0].new_start == 1.0  # preroll offset preserved
    assert plans[0].video_speed == 1.0


def test_plan_timeline_empty():
    assert plan_timeline([], video_total=5.0) == []
