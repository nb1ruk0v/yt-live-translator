from unittest.mock import MagicMock, patch

from merge import merge
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
    """Regression guard: ATEMPO_MAX cap value (currently 1.5)."""
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
    assert abs(atempo_calls[0].args[1] - 1.5) < 1e-6


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
