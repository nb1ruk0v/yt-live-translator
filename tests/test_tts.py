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


@patch("tts._wav_duration", return_value=1.0)
@patch("tts.TTS")
def test_synthesize_fills_audio_path(mock_tts_cls, _mock_dur):
    mock_tts_cls.return_value = MagicMock()

    segments = make_segments()
    result = synthesize(segments, FAKE_CONFIG)

    assert result[0].audio_path != ""
    assert result[1].audio_path != ""
    assert result[0].audio_path.endswith(".wav")


@patch("tts._wav_duration", return_value=1.0)
@patch("tts.TTS")
def test_synthesize_calls_tts_with_translated(mock_tts_cls, _mock_dur):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance

    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG)

    call_kwargs = mock_instance.tts_to_file.call_args[1]
    assert call_kwargs["text"] == "Привет"
    assert call_kwargs["language"] == "ru"


@patch("tts._wav_duration", return_value=1.0)
@patch("tts.TTS")
def test_synthesize_passes_speaker_wav_when_set(mock_tts_cls, _mock_dur):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance

    config = {**FAKE_CONFIG, "speaker_wav": "/path/to/speaker.wav"}
    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, config)

    call_kwargs = mock_instance.tts_to_file.call_args[1]
    assert call_kwargs["speaker_wav"] == "/path/to/speaker.wav"


@patch("tts._wav_duration", return_value=1.0)
@patch("tts.TTS")
def test_synthesize_no_speaker_wav_when_null(mock_tts_cls, _mock_dur):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance

    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG)

    call_kwargs = mock_instance.tts_to_file.call_args[1]
    assert "speaker_wav" not in call_kwargs


@patch("tts.TTS")
def test_synthesize_uses_config_model(mock_tts_cls):
    mock_tts_cls.return_value = MagicMock()

    synthesize([], FAKE_CONFIG)

    mock_tts_cls.assert_called_once_with(
        "tts_models/multilingual/multi-dataset/xtts_v2"
    )


@patch("tts._wav_duration", return_value=1.0)
@patch("tts.TTS")
def test_synthesize_first_pass_uses_speed_1(mock_tts_cls, _mock_dur):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance

    segments = [Segment(start=0.0, end=2.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG)

    first_kwargs = mock_instance.tts_to_file.call_args_list[0][1]
    assert first_kwargs["speed"] == 1.0


@patch("tts._wav_duration")
@patch("tts.TTS")
def test_synthesize_populates_audio_duration(mock_tts_cls, mock_dur):
    mock_tts_cls.return_value = MagicMock()
    mock_dur.return_value = 1.4

    segments = [Segment(start=0.0, end=2.0, original="Hi", translated="Привет")]
    result = synthesize(segments, FAKE_CONFIG)

    assert result[0].audio_duration == 1.4


@patch("tts._wav_duration")
@patch("tts.TTS")
def test_synthesize_no_resynth_when_fits(mock_tts_cls, mock_dur):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance
    mock_dur.return_value = 1.5  # window is 2.0 — fits

    segments = [Segment(start=0.0, end=2.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG)

    assert mock_instance.tts_to_file.call_count == 1


@patch("tts._wav_duration")
@patch("tts.TTS")
def test_synthesize_resynth_when_too_long(mock_tts_cls, mock_dur):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance
    # first probe: 3.0 (window is 2.0 → speed=1.2 clamp), second probe: 2.5
    mock_dur.side_effect = [3.0, 2.5]

    segments = [Segment(start=0.0, end=2.0, original="Hi", translated="Привет")]
    result = synthesize(segments, FAKE_CONFIG)

    assert mock_instance.tts_to_file.call_count == 2
    second_kwargs = mock_instance.tts_to_file.call_args_list[1][1]
    assert second_kwargs["speed"] == 1.2  # clamped
    assert result[0].audio_duration == 2.5


@patch("tts._wav_duration")
@patch("tts.TTS")
def test_synthesize_resynth_speed_unclamped_when_in_range(mock_tts_cls, mock_dur):
    mock_instance = MagicMock()
    mock_tts_cls.return_value = mock_instance
    # first: 2.2 over window 2.0 → speed=1.1 (within clamp)
    mock_dur.side_effect = [2.2, 2.0]

    segments = [Segment(start=0.0, end=2.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG)

    second_kwargs = mock_instance.tts_to_file.call_args_list[1][1]
    assert abs(second_kwargs["speed"] - 1.1) < 1e-6
