from unittest.mock import patch, MagicMock
from segment import Segment
from merge import merge


def make_segments():
    return [
        Segment(
            start=0.0, end=2.0,
            original="Hi", translated="Привет",
            audio_path="/tmp/seg_0000.wav", audio_duration=1.8,
        ),
        Segment(
            start=3.0, end=5.0,
            original="Bye", translated="Пока",
            audio_path="/tmp/seg_0001.wav", audio_duration=1.5,
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
def test_merge_returns_output_path(mock_ffmpeg):
    _setup(mock_ffmpeg)
    result = merge("/videos/test.mp4", make_segments(), "_dubbed")
    assert result == "/videos/test_dubbed.mp4"


@patch("merge.ffmpeg")
def test_merge_output_path_uses_suffix(mock_ffmpeg):
    _setup(mock_ffmpeg)
    result = merge("/videos/movie.mp4", make_segments(), "_ru")
    assert result == "/videos/movie_ru.mp4"


@patch("merge.ffmpeg")
def test_merge_calls_run(mock_ffmpeg):
    _setup(mock_ffmpeg)
    merge("/videos/test.mp4", make_segments(), "_dubbed")
    mock_ffmpeg.output.return_value.overwrite_output.return_value.run.assert_called_once_with(
        capture_stdout=True, capture_stderr=True
    )


@patch("merge.ffmpeg")
def test_merge_no_atrim_when_audio_fits(mock_ffmpeg):
    chain = _setup(mock_ffmpeg)
    merge("/videos/test.mp4", make_segments(), "_dubbed")
    # audio fits in both segments — no stretch and no cap needed
    assert "atrim" not in _filter_names(chain)


@patch("merge.ffmpeg")
def test_merge_no_atempo_when_audio_fits(mock_ffmpeg):
    chain = _setup(mock_ffmpeg)
    merge("/videos/test.mp4", make_segments(), "_dubbed")
    assert "atempo" not in _filter_names(chain)


@patch("merge.ffmpeg")
def test_merge_atrim_caps_when_stretched(mock_ffmpeg):
    chain = _setup(mock_ffmpeg)
    segs = [Segment(
        start=0.0, end=2.0,
        original="Hi", translated="Привет",
        audio_path="/tmp/x.wav", audio_duration=3.0,
    )]
    merge("/videos/test.mp4", segs, "_dubbed")

    atrim_calls = [c for c in chain.filter.call_args_list if c.args[0] == "atrim"]
    assert len(atrim_calls) == 1
    assert atrim_calls[0].kwargs == {"duration": 2.0}


@patch("merge.ffmpeg")
def test_merge_atempo_when_audio_too_long(mock_ffmpeg):
    chain = _setup(mock_ffmpeg)
    segs = [Segment(
        start=0.0, end=2.0,
        original="Hi", translated="Привет",
        audio_path="/tmp/x.wav", audio_duration=2.2,
    )]
    merge("/videos/test.mp4", segs, "_dubbed")

    atempo_calls = [c for c in chain.filter.call_args_list if c.args[0] == "atempo"]
    assert len(atempo_calls) == 1
    assert abs(atempo_calls[0].args[1] - 1.1) < 1e-6


@patch("merge.ffmpeg")
def test_merge_atempo_clamped_to_upper(mock_ffmpeg):
    chain = _setup(mock_ffmpeg)
    segs = [Segment(
        start=0.0, end=2.0,
        original="Hi", translated="Привет",
        audio_path="/tmp/x.wav", audio_duration=3.0,
    )]
    merge("/videos/test.mp4", segs, "_dubbed")

    atempo_calls = [c for c in chain.filter.call_args_list if c.args[0] == "atempo"]
    assert len(atempo_calls) == 1
    assert abs(atempo_calls[0].args[1] - 1.15) < 1e-6


@patch("merge.ffmpeg")
def test_merge_adelay_still_applied(mock_ffmpeg):
    chain = _setup(mock_ffmpeg)
    merge("/videos/test.mp4", make_segments(), "_dubbed")
    assert "adelay" in _filter_names(chain)
