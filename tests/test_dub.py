from unittest.mock import patch

import pytest

import dub
from segment import Segment

FAKE_SEGMENTS = [
    Segment(
        start=0.0,
        end=2.0,
        original="Hello",
        translated="Привет",
        audio_path="/tmp/seg_0000.wav",
    ),
]

FAKE_CONFIG = {
    "transcription": {"model": "base", "device": "cpu", "language": "auto"},
    "translation": {"model": "llama3.2:3b", "ollama_url": "http://localhost:11434"},
    "tts": {"model": "xtts_v2", "language": "ru", "speaker_wav": None},
    "output": {"suffix": "_dubbed"},
}


@patch("dub.merge")
@patch("dub.synthesize")
@patch("dub.translate")
@patch("dub.transcribe")
@patch("dub.check_prerequisites")
@patch("dub.load_config")
@patch("pathlib.Path.exists", return_value=True)
def test_main_full_pipeline(
    mock_exists,
    mock_config,
    mock_check,
    mock_transcribe,
    mock_translate,
    mock_synthesize,
    mock_merge,
):
    mock_config.return_value = FAKE_CONFIG
    mock_transcribe.return_value = FAKE_SEGMENTS
    mock_translate.return_value = FAKE_SEGMENTS
    mock_synthesize.return_value = FAKE_SEGMENTS
    mock_merge.return_value = "/tmp/video_dubbed.mp4"

    with patch("sys.argv", ["dub.py", "/tmp/video.mp4"]):
        dub.main()

    mock_transcribe.assert_called_once()
    mock_translate.assert_called_once_with(FAKE_SEGMENTS, FAKE_CONFIG["translation"])
    mock_synthesize.assert_called_once_with(FAKE_SEGMENTS, FAKE_CONFIG["tts"])
    mock_merge.assert_called_once_with("/tmp/video.mp4", FAKE_SEGMENTS, "_dubbed")


def test_main_exits_if_no_args():
    with patch("sys.argv", ["dub.py"]):
        with pytest.raises(SystemExit) as exc_info:
            dub.main()
        assert exc_info.value.code == 1


@patch("dub.load_config")
@patch("pathlib.Path.exists", return_value=False)
def test_main_exits_if_file_not_found(mock_exists, mock_config):
    mock_config.return_value = FAKE_CONFIG
    with patch("sys.argv", ["dub.py", "/nonexistent/video.mp4"]):
        with pytest.raises(SystemExit) as exc_info:
            dub.main()
        assert exc_info.value.code == 1
