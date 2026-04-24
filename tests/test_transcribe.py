from unittest.mock import MagicMock, patch

from segment import Segment
from transcribe import transcribe

FAKE_CONFIG = {
    "model": "base",
    "device": "cpu",
    "language": "auto",
}


def make_fake_whisper_segment(start, end, text):
    seg = MagicMock()
    seg.start = start
    seg.end = end
    seg.text = f"  {text}  "  # с пробелами — проверяем strip()
    return seg


@patch("transcribe.WhisperModel")
@patch("transcribe.subprocess.run")
def test_transcribe_returns_segments(mock_run, mock_model_cls):
    mock_run.return_value = MagicMock(returncode=0)

    fake_segments = [
        make_fake_whisper_segment(0.0, 2.0, "Hello world"),
        make_fake_whisper_segment(2.5, 5.0, "How are you"),
    ]
    mock_instance = MagicMock()
    mock_instance.transcribe.return_value = (iter(fake_segments), MagicMock())
    mock_model_cls.return_value = mock_instance

    result = transcribe("video.mp4", FAKE_CONFIG)

    assert len(result) == 2
    assert isinstance(result[0], Segment)
    assert result[0].start == 0.0
    assert result[0].end == 2.0
    assert result[0].original == "Hello world"
    assert result[1].original == "How are you"


@patch("transcribe.WhisperModel")
@patch("transcribe.subprocess.run")
def test_transcribe_calls_ffmpeg(mock_run, mock_model_cls):
    mock_run.return_value = MagicMock(returncode=0)
    mock_instance = MagicMock()
    mock_instance.transcribe.return_value = (iter([]), MagicMock())
    mock_model_cls.return_value = mock_instance

    transcribe("my_video.mp4", FAKE_CONFIG)

    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]
    assert "ffmpeg" in call_args
    assert "my_video.mp4" in call_args
    assert "-ac" in call_args
    assert "1" in call_args
    assert "-ar" in call_args
    assert "16000" in call_args
    assert "-vn" in call_args


@patch("transcribe.WhisperModel")
@patch("transcribe.subprocess.run")
def test_transcribe_uses_config_model(mock_run, mock_model_cls):
    mock_run.return_value = MagicMock(returncode=0)
    mock_instance = MagicMock()
    mock_instance.transcribe.return_value = (iter([]), MagicMock())
    mock_model_cls.return_value = mock_instance

    config = {**FAKE_CONFIG, "model": "large-v3", "device": "cuda"}
    transcribe("video.mp4", config)

    mock_model_cls.assert_called_once_with("large-v3", device="cuda", compute_type="int8")
