from unittest.mock import patch

import diarize
from diarize import _assign_speaker
from segment import Segment


def test_max_overlap_picks_dominant_speaker():
    intervals = [
        (0.0, 1.0, "SPEAKER_00"),
        (1.0, 5.0, "SPEAKER_01"),
    ]
    # segment 0..4 overlaps SPEAKER_00 by 1s, SPEAKER_01 by 3s
    assert _assign_speaker(0.0, 4.0, intervals) == "SPEAKER_01"


def test_no_overlap_returns_unknown():
    intervals = [
        (0.0, 1.0, "SPEAKER_00"),
        (10.0, 12.0, "SPEAKER_01"),
    ]
    assert _assign_speaker(5.0, 6.0, intervals) == "SPEAKER_UNKNOWN"


def test_partial_overlap_counted_correctly():
    intervals = [
        (0.0, 5.0, "SPEAKER_00"),
        (4.5, 10.0, "SPEAKER_01"),
    ]
    # segment 4..6: overlaps SPEAKER_00 by 1.0, SPEAKER_01 by 1.5
    assert _assign_speaker(4.0, 6.0, intervals) == "SPEAKER_01"


def test_segment_fully_inside_one_interval():
    intervals = [(0.0, 100.0, "SPEAKER_00")]
    assert _assign_speaker(10.0, 20.0, intervals) == "SPEAKER_00"


def test_empty_intervals_returns_unknown():
    assert _assign_speaker(0.0, 1.0, []) == "SPEAKER_UNKNOWN"


@patch("diarize.subprocess.run")
@patch("diarize.os.path.exists", return_value=True)
def test_ensure_audio_returns_existing_path_without_ffmpeg(mock_exists, mock_run):
    path = diarize._ensure_audio("/tmp/clip.mp4")
    assert path == "/tmp/clip.wav"
    mock_run.assert_not_called()


@patch("diarize.subprocess.run")
@patch("diarize.os.path.exists", return_value=False)
def test_ensure_audio_extracts_when_missing(mock_exists, mock_run):
    mock_run.return_value.returncode = 0

    path = diarize._ensure_audio("/tmp/clip.mp4")

    assert path == "/tmp/clip.wav"
    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert cmd[0] == "ffmpeg"
    assert "/tmp/clip.mp4" in cmd
    assert "/tmp/clip.wav" in cmd
    assert "22050" in cmd  # sample rate


@patch("diarize._ensure_audio", return_value="/tmp/clip.wav")
@patch("diarize.Pipeline")
@patch.dict("os.environ", {"HUGGINGFACE_TOKEN": "fake-token"})
def test_diarize_assigns_speaker_per_segment(mock_pipeline_cls, _mock_audio):
    pipeline = mock_pipeline_cls.from_pretrained.return_value

    fake_diarization = [
        ((0.0, 2.0), None, "SPEAKER_00"),
        ((2.0, 5.0), None, "SPEAKER_01"),
    ]

    class FakeAnnotation:
        def itertracks(self, yield_label):
            for turn_range, _, speaker in fake_diarization:
                turn = type("Turn", (), {"start": turn_range[0], "end": turn_range[1]})()
                yield turn, None, speaker

    pipeline.return_value = FakeAnnotation()

    segments = [
        Segment(start=0.5, end=1.5, original="hi"),
        Segment(start=3.0, end=4.0, original="there"),
    ]

    config = {
        "model": "pyannote/speaker-diarization-3.1",
        "hf_token_env": "HUGGINGFACE_TOKEN",
    }

    result = diarize.diarize("/tmp/clip.mp4", segments, config)

    assert result[0].speaker == "SPEAKER_00"
    assert result[1].speaker == "SPEAKER_01"
    mock_pipeline_cls.from_pretrained.assert_called_once_with(
        "pyannote/speaker-diarization-3.1",
        token="fake-token",
    )


@patch("diarize._ensure_audio", return_value="/tmp/clip.wav")
@patch("diarize.Pipeline")
@patch.dict("os.environ", {}, clear=True)
def test_diarize_raises_without_token(mock_pipeline_cls, _mock_audio):
    segments = [Segment(start=0.0, end=1.0, original="hi")]
    config = {
        "model": "pyannote/speaker-diarization-3.1",
        "hf_token_env": "HUGGINGFACE_TOKEN",
    }

    import pytest

    with pytest.raises(RuntimeError, match="HUGGINGFACE_TOKEN"):
        diarize.diarize("/tmp/clip.mp4", segments, config)
