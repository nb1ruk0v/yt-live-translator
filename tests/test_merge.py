from unittest.mock import patch, MagicMock
from segment import Segment
from merge import merge


def make_segments():
    return [
        Segment(start=0.0, end=2.0, original="Hi", translated="Привет", audio_path="/tmp/seg_0000.wav"),
        Segment(start=3.0, end=5.0, original="Bye", translated="Пока", audio_path="/tmp/seg_0001.wav"),
    ]


@patch("merge.ffmpeg")
def test_merge_returns_output_path(mock_ffmpeg):
    mock_ffmpeg.input.return_value = MagicMock()
    mock_ffmpeg.filter.return_value = MagicMock()
    mock_out = MagicMock()
    mock_ffmpeg.output.return_value = mock_out
    mock_out.overwrite_output.return_value = mock_out

    result = merge("/videos/test.mp4", make_segments(), "_dubbed")

    assert result == "/videos/test_dubbed.mp4"


@patch("merge.ffmpeg")
def test_merge_output_path_uses_suffix(mock_ffmpeg):
    mock_ffmpeg.input.return_value = MagicMock()
    mock_ffmpeg.filter.return_value = MagicMock()
    mock_out = MagicMock()
    mock_ffmpeg.output.return_value = mock_out
    mock_out.overwrite_output.return_value = mock_out

    result = merge("/videos/movie.mp4", make_segments(), "_ru")

    assert result == "/videos/movie_ru.mp4"


@patch("merge.ffmpeg")
def test_merge_calls_run(mock_ffmpeg):
    mock_ffmpeg.input.return_value = MagicMock()
    mock_ffmpeg.filter.return_value = MagicMock()
    mock_out = MagicMock()
    mock_ffmpeg.output.return_value = mock_out
    mock_out.overwrite_output.return_value = mock_out

    merge("/videos/test.mp4", make_segments(), "_dubbed")

    mock_out.overwrite_output.return_value.run.assert_called_once_with(
        capture_stdout=True, capture_stderr=True
    )
