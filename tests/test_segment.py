from segment import Segment


def test_segment_defaults():
    seg = Segment(start=0.0, end=2.5, original="Hello world")
    assert seg.start == 0.0
    assert seg.end == 2.5
    assert seg.original == "Hello world"
    assert seg.translated == ""
    assert seg.audio_path == ""


def test_segment_full():
    seg = Segment(
        start=1.0,
        end=3.0,
        original="Hello",
        translated="Привет",
        audio_path="/tmp/seg_0000.wav",
    )
    assert seg.translated == "Привет"
    assert seg.audio_path == "/tmp/seg_0000.wav"


def test_segment_duration():
    seg = Segment(start=1.5, end=4.5, original="test")
    assert seg.duration == 3.0
