from unittest.mock import MagicMock, patch

from segment import Segment
from tts import synthesize

FAKE_CONFIG = {
    "model": "tts_models/multilingual/multi-dataset/xtts_v2",
    "language": "ru",
    "device": "cpu",
    "reference_seconds": 10,
}


def make_segments():
    return [
        Segment(start=0.0, end=2.0, original="Hello", translated="Привет"),
        Segment(start=2.5, end=5.0, original="World", translated="Мир"),
    ]


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
def test_synthesize_fills_audio_path(mock_load, _mock_ref, _mock_dur):
    mock_load.return_value = MagicMock()

    result = synthesize(make_segments(), FAKE_CONFIG, "/tmp/video.mp4")

    assert result[0].audio_path.endswith(".wav")
    assert result[1].audio_path.endswith(".wav")


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
def test_synthesize_passes_text_and_reference(mock_load, _mock_ref, _mock_dur):
    model = MagicMock()
    mock_load.return_value = model

    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG, "/tmp/video.mp4")

    kwargs = model.tts_to_file.call_args[1]
    assert kwargs["text"] == "Привет"
    assert kwargs["speaker_wav"] == "/tmp/video_ref.wav"
    assert kwargs["language"] == "ru"


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
def test_synthesize_populates_audio_duration(mock_load, _mock_ref, mock_dur):
    mock_load.return_value = MagicMock()
    mock_dur.return_value = 1.7

    segments = [Segment(start=0.0, end=2.0, original="Hi", translated="Привет")]
    result = synthesize(segments, FAKE_CONFIG, "/tmp/video.mp4")

    assert result[0].audio_duration == 1.7


@patch("tts._wav_duration", return_value=0.05)
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
@patch("tts._write_silence")
def test_synthesize_writes_silence_for_empty_translation(
    mock_silence, mock_load, _mock_ref, _mock_dur
):
    model = MagicMock()
    mock_load.return_value = model

    segments = [Segment(start=0.0, end=1.0, original="...", translated="")]
    synthesize(segments, FAKE_CONFIG, "/tmp/video.mp4")

    mock_silence.assert_called_once()
    model.tts_to_file.assert_not_called()
