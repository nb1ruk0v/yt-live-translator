from unittest.mock import patch

import diarize
from diarize import _assign_speaker


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
