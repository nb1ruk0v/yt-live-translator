from unittest.mock import MagicMock, patch

import tts
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
@patch("tts._extract_per_speaker_references", return_value={})
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
def test_synthesize_fills_audio_path(mock_load, _mock_ref, _mock_per_speaker, _mock_dur):
    mock_load.return_value = MagicMock()

    result = synthesize(make_segments(), FAKE_CONFIG, "/tmp/video.mp4")

    assert result[0].audio_path.endswith(".wav")
    assert result[1].audio_path.endswith(".wav")


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._extract_per_speaker_references", return_value={})
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
def test_synthesize_passes_text_and_reference(mock_load, _mock_ref, _mock_per_speaker, _mock_dur):
    model = MagicMock()
    mock_load.return_value = model

    segments = [Segment(start=0.0, end=1.0, original="Hi", translated="Привет")]
    synthesize(segments, FAKE_CONFIG, "/tmp/video.mp4")

    kwargs = model.tts_to_file.call_args[1]
    assert kwargs["text"] == "Привет"
    assert kwargs["speaker_wav"] == "/tmp/video_ref.wav"
    assert kwargs["language"] == "ru"


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._extract_per_speaker_references", return_value={})
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
def test_synthesize_populates_audio_duration(mock_load, _mock_ref, _mock_per_speaker, mock_dur):
    mock_load.return_value = MagicMock()
    mock_dur.return_value = 1.7

    segments = [Segment(start=0.0, end=2.0, original="Hi", translated="Привет")]
    result = synthesize(segments, FAKE_CONFIG, "/tmp/video.mp4")

    assert result[0].audio_duration == 1.7


@patch("tts._wav_duration", return_value=0.05)
@patch("tts._extract_per_speaker_references", return_value={})
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
@patch("tts._write_silence")
def test_synthesize_writes_silence_for_empty_translation(
    mock_silence, mock_load, _mock_ref, _mock_per_speaker, _mock_dur
):
    model = MagicMock()
    mock_load.return_value = model

    segments = [Segment(start=0.0, end=1.0, original="...", translated="")]
    synthesize(segments, FAKE_CONFIG, "/tmp/video.mp4")

    mock_silence.assert_called_once()
    model.tts_to_file.assert_not_called()


@patch("tts.subprocess.run")
def test_per_speaker_refs_extracts_each_unique_speaker(mock_run):
    mock_run.return_value.returncode = 0
    segments = [
        Segment(start=0.0, end=4.0, original="A", speaker="SPEAKER_00"),
        Segment(start=4.0, end=8.0, original="B", speaker="SPEAKER_01"),
        Segment(start=8.0, end=12.0, original="C", speaker="SPEAKER_00"),
    ]

    refs = tts._extract_per_speaker_references(
        "/tmp/video.mp4",
        segments,
        target_seconds=10.0,
        min_seconds=3.0,
    )

    assert set(refs.keys()) == {"SPEAKER_00", "SPEAKER_01"}
    assert refs["SPEAKER_00"].endswith("_ref_SPEAKER_00.wav")
    assert refs["SPEAKER_01"].endswith("_ref_SPEAKER_01.wav")
    assert mock_run.call_count == 2  # one ffmpeg call per speaker


@patch("tts.subprocess.run")
def test_per_speaker_refs_picks_longest_continuous_run(mock_run):
    mock_run.return_value.returncode = 0
    # SPEAKER_00 has two runs: 0..1 (1s) and 4..10 (6s) — 4..10 must be picked.
    segments = [
        Segment(start=0.0, end=1.0, original="A", speaker="SPEAKER_00"),
        Segment(start=1.0, end=4.0, original="B", speaker="SPEAKER_01"),
        Segment(start=4.0, end=7.0, original="C", speaker="SPEAKER_00"),
        Segment(start=7.0, end=10.0, original="D", speaker="SPEAKER_00"),
    ]

    tts._extract_per_speaker_references(
        "/tmp/video.mp4",
        segments,
        target_seconds=10.0,
        min_seconds=3.0,
    )

    speaker_00_call = next(
        c for c in mock_run.call_args_list if any("_ref_SPEAKER_00.wav" in s for s in c[0][0])
    )
    cmd = speaker_00_call[0][0]
    ss_idx = cmd.index("-ss")
    assert float(cmd[ss_idx + 1]) == 4.0


@patch("tts.subprocess.run")
def test_per_speaker_refs_falls_back_for_short_runs(mock_run, capsys):
    mock_run.return_value.returncode = 0
    # SPEAKER_01 has only a 1.5s run — under min_seconds=3.0 → fallback to SPEAKER_00.
    segments = [
        Segment(start=0.0, end=10.0, original="A", speaker="SPEAKER_00"),
        Segment(start=10.0, end=11.5, original="B", speaker="SPEAKER_01"),
    ]

    refs = tts._extract_per_speaker_references(
        "/tmp/video.mp4",
        segments,
        target_seconds=10.0,
        min_seconds=3.0,
    )

    assert refs["SPEAKER_01"] == refs["SPEAKER_00"]  # deterministic fallback
    captured = capsys.readouterr()
    assert "SPEAKER_01" in captured.err  # warning printed


@patch("tts.subprocess.run")
def test_per_speaker_refs_caps_clip_at_target_seconds(mock_run):
    mock_run.return_value.returncode = 0
    segments = [
        Segment(start=0.0, end=60.0, original="A", speaker="SPEAKER_00"),
    ]

    tts._extract_per_speaker_references(
        "/tmp/video.mp4",
        segments,
        target_seconds=10.0,
        min_seconds=3.0,
    )

    cmd = mock_run.call_args_list[0][0][0]
    to_idx = cmd.index("-to")
    assert float(cmd[to_idx + 1]) == 10.0


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._extract_per_speaker_references")
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
def test_synthesize_uses_per_speaker_ref_when_available(
    mock_load, _mock_legacy_ref, mock_per_speaker, _mock_dur
):
    model = MagicMock()
    mock_load.return_value = model
    mock_per_speaker.return_value = {
        "SPEAKER_00": "/tmp/ref_00.wav",
        "SPEAKER_01": "/tmp/ref_01.wav",
    }

    segments = [
        Segment(start=0.0, end=1.0, original="hi", translated="привет", speaker="SPEAKER_00"),
        Segment(start=1.0, end=2.0, original="bye", translated="пока", speaker="SPEAKER_01"),
    ]
    synthesize(segments, FAKE_CONFIG, "/tmp/video.mp4")

    speaker_wavs = [c[1]["speaker_wav"] for c in model.tts_to_file.call_args_list]
    assert speaker_wavs == ["/tmp/ref_00.wav", "/tmp/ref_01.wav"]


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._extract_per_speaker_references")
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
def test_synthesize_falls_back_to_legacy_when_no_speakers(
    mock_load, _mock_legacy_ref, mock_per_speaker, _mock_dur
):
    model = MagicMock()
    mock_load.return_value = model
    mock_per_speaker.return_value = {}  # no diarization happened

    segments = [
        Segment(start=0.0, end=1.0, original="hi", translated="привет"),
    ]
    synthesize(segments, FAKE_CONFIG, "/tmp/video.mp4")

    kwargs = model.tts_to_file.call_args[1]
    assert kwargs["speaker_wav"] == "/tmp/video_ref.wav"


@patch("tts._wav_duration", return_value=1.0)
@patch("tts._extract_per_speaker_references")
@patch("tts._extract_reference", return_value="/tmp/video_ref.wav")
@patch("tts._load_model")
def test_synthesize_falls_back_to_first_ref_for_unknown_speaker(
    mock_load, _mock_legacy_ref, mock_per_speaker, _mock_dur
):
    model = MagicMock()
    mock_load.return_value = model
    mock_per_speaker.return_value = {"SPEAKER_00": "/tmp/ref_00.wav"}

    segments = [
        Segment(
            start=0.0,
            end=1.0,
            original="hi",
            translated="привет",
            speaker="SPEAKER_UNKNOWN",
        ),
    ]
    synthesize(segments, FAKE_CONFIG, "/tmp/video.mp4")

    kwargs = model.tts_to_file.call_args[1]
    assert kwargs["speaker_wav"] == "/tmp/ref_00.wav"
