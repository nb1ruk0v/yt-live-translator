from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from segment import Segment
from transcribe import _resegment, transcribe

FAKE_CONFIG = {
    "model": "base",
    "device": "cpu",
    "language": "auto",
}


def W(start: float, end: float, word: str) -> SimpleNamespace:
    """Build a fake faster-whisper Word."""
    return SimpleNamespace(start=start, end=end, word=word)


def fake_whisper_segment(words: list) -> SimpleNamespace:
    """Wrap words into a faster-whisper-like Segment (only .words is read)."""
    return SimpleNamespace(words=words)


# ---------- _resegment ----------


class TestResegment:
    def test_empty_input(self):
        assert _resegment([]) == []

    def test_splits_on_sentence_end(self):
        # two sentences, no pause between — split on the period.
        words = [
            W(0.0, 0.3, "Hi"),
            W(0.3, 0.7, " everyone."),
            W(0.7, 1.0, " My"),
            W(1.0, 1.4, " name"),
            W(1.4, 1.6, " is"),
            W(1.6, 2.0, " Hannah."),
        ]
        out = _resegment(words, min_duration=0.5)
        assert len(out) == 2
        assert out[0].original == "Hi everyone."
        assert out[1].original == "My name is Hannah."
        assert out[0].end == 0.7
        assert out[1].start == 0.7

    def test_splits_on_long_pause_without_punctuation(self):
        words = [
            W(0.0, 0.5, "Hello"),
            W(0.5, 1.0, " world"),
            # 0.6s pause — exceeds default 0.4 threshold
            W(1.6, 2.0, " How"),
            W(2.0, 2.4, " are"),
            W(2.4, 2.8, " you"),
        ]
        out = _resegment(words, min_duration=0.5)
        assert len(out) == 2
        assert out[0].original == "Hello world"
        assert out[1].original == "How are you"

    def test_caps_at_max_duration(self):
        # one long monotonic stream, no punctuation, no pauses → forced split.
        words = [W(i * 0.5, (i + 1) * 0.5, f" w{i}") for i in range(20)]  # 10s total
        out = _resegment(words, max_duration=4.0, min_duration=1.0)
        assert len(out) >= 2
        for s in out:
            assert s.duration <= 4.5  # exact split happens once buffer crosses cap

    def test_does_not_split_below_min_duration(self):
        # period right after start — must NOT split, stays under min_duration.
        words = [
            W(0.0, 0.2, "Hi."),
            W(0.5, 1.0, " Then"),
            W(1.0, 1.5, " more"),
            W(1.5, 2.0, " words."),
        ]
        out = _resegment(words, min_duration=1.0)
        # "Hi." is at 0.2s — under min_duration, must merge into next.
        assert len(out) == 1
        assert out[0].original == "Hi. Then more words."

    def test_flushes_remainder_below_min_duration(self):
        # tail under min_duration still emitted (don't drop content).
        words = [
            W(0.0, 1.5, "Long sentence here."),
            W(2.0, 2.3, " Tail"),
        ]
        out = _resegment(words, min_duration=1.0, pause_threshold=0.4)
        assert len(out) == 2
        assert out[1].original == "Tail"


# ---------- transcribe (integration with mocked Whisper) ----------


@patch("transcribe.WhisperModel")
@patch("transcribe.subprocess.run")
def test_transcribe_uses_word_timestamps_and_returns_resegmented(mock_run, mock_model_cls):
    mock_run.return_value = MagicMock(returncode=0)

    # one whisper segment with word timestamps; resegmenter splits on the period.
    whisper_seg = fake_whisper_segment(
        [
            W(0.0, 0.5, "Hello"),
            W(0.5, 1.0, " world."),
            W(1.5, 2.0, " Bye"),
        ]
    )
    mock_instance = MagicMock()
    mock_instance.transcribe.return_value = (iter([whisper_seg]), MagicMock())
    mock_model_cls.return_value = mock_instance

    result = transcribe("video.mp4", FAKE_CONFIG)

    # word_timestamps and vad_filter must be on
    assert mock_instance.transcribe.call_args[1]["word_timestamps"] is True
    assert mock_instance.transcribe.call_args[1]["vad_filter"] is True

    assert len(result) == 2
    assert isinstance(result[0], Segment)
    assert result[0].original == "Hello world."
    assert result[1].original == "Bye"
