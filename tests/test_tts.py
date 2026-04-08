import os
import tempfile
from unittest.mock import patch, MagicMock
from segment import Segment
from tts import synthesize


FAKE_CONFIG = {
    "model": "tts_models/multilingual/multi-dataset/xtts_v2",
    "language": "ru",
    "speaker_wav": None,
}


def make_segments():
    return [
        Segment(start=0.0, end=2.0, original="Hello", translated="Привет"),
        Segment(start=2.5, end=5.0, original="World", translated="Мир"),
    ]


@patch("tts.TTS")
def test_synthesize_fills_audio_path(mock_tts_cls):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance

    segments = make_segments()
    result = synthesize(segments, FAKE_CONFIG)

    assert result[0].audio_path != ""
    assert result[1].audio_path != ""
    assert result[0].audio_path.endswith(".wav")


@patch("tts.TTS")
def test_synthesize_calls_tts_with_translated(mock_tts_cls):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance

    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG)

    call_kwargs = mock_instance.tts_to_file.call_args[1]
    assert call_kwargs["text"] == "Привет"
    assert call_kwargs["language"] == "ru"


@patch("tts.TTS")
def test_synthesize_passes_speaker_wav_when_set(mock_tts_cls):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance

    config = {**FAKE_CONFIG, "speaker_wav": "/path/to/speaker.wav"}
    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, config)

    call_kwargs = mock_instance.tts_to_file.call_args[1]
    assert call_kwargs["speaker_wav"] == "/path/to/speaker.wav"


@patch("tts.TTS")
def test_synthesize_no_speaker_wav_when_null(mock_tts_cls):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance

    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG)

    call_kwargs = mock_instance.tts_to_file.call_args[1]
    assert "speaker_wav" not in call_kwargs


@patch("tts.TTS")
def test_synthesize_uses_config_model(mock_tts_cls):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance

    synthesize([], FAKE_CONFIG)

    mock_tts_cls.assert_called_once_with(
        "tts_models/multilingual/multi-dataset/xtts_v2"
    )
