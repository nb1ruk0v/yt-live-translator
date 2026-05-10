from segment import Segment


def test_speaker_default_empty():
    seg = Segment(start=0.0, end=1.0, original="Hi")
    assert seg.speaker == ""


def test_speaker_can_be_set():
    seg = Segment(start=0.0, end=1.0, original="Hi", speaker="SPEAKER_00")
    assert seg.speaker == "SPEAKER_00"
