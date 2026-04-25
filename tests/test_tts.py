from unittest.mock import MagicMock, patch

from segment import Segment
from tts import synthesize

FAKE_CONFIG = {
    "model": "v4_ru",
    "language": "ru",
    "speaker": "eugene",
    "sample_rate": 48000,
}


def make_segments():
    return [
        Segment(start=0.0, end=2.0, original="Hello", translated="Привет"),
        Segment(start=2.5, end=5.0, original="World", translated="Мир"),
    ]


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._save_wav")
@patch("tts._load_model")
def test_synthesize_fills_audio_path(mock_load, _mock_ta, _mock_dur):
    mock_load.return_value = MagicMock()

    result = synthesize(make_segments(), FAKE_CONFIG)

    assert result[0].audio_path.endswith(".wav")
    assert result[1].audio_path.endswith(".wav")


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._save_wav")
@patch("tts._load_model")
def test_synthesize_passes_text_and_speaker(mock_load, _mock_ta, _mock_dur):
    model = MagicMock()
    mock_load.return_value = model

    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG)

    kwargs = model.apply_tts.call_args[1]
    assert kwargs["text"] == "Привет"
    assert kwargs["speaker"] == "eugene"
    assert kwargs["sample_rate"] == 48000


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._save_wav")
@patch("tts._load_model")
def test_synthesize_default_sample_rate(mock_load, _mock_ta, _mock_dur):
    model = MagicMock()
    mock_load.return_value = model

    config = {k: v for k, v in FAKE_CONFIG.items() if k != "sample_rate"}
    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, config)

    assert model.apply_tts.call_args[1]["sample_rate"] == 48000


@patch("tts._wav_duration")
@patch("tts._save_wav")
@patch("tts._load_model")
def test_synthesize_populates_audio_duration(mock_load, _mock_ta, mock_dur):
    mock_load.return_value = MagicMock()
    mock_dur.return_value = 1.7

    segments = [Segment(start=0.0, end=2.0, original="Hi", translated="Привет")]
    result = synthesize(segments, FAKE_CONFIG)

    assert result[0].audio_duration == 1.7


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._save_wav")
@patch("tts._load_model")
def test_synthesize_saves_wav(mock_load, mock_save, _mock_dur):
    mock_load.return_value = MagicMock()

    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG)

    assert mock_save.called
    save_args = mock_save.call_args
    assert save_args.args[0].endswith(".wav")
    assert save_args.args[2] == 48000
