from segment import Segment
from subtitles import _escape, _format_timecode, _wrap, write_srt


class TestFormatTimecode:
    def test_zero(self):
        assert _format_timecode(0.0) == "00:00:00,000"

    def test_subsecond_milliseconds(self):
        assert _format_timecode(1.234) == "00:00:01,234"

    def test_hours_minutes_seconds(self):
        # 1h 1m 1.5s
        assert _format_timecode(3661.5) == "01:01:01,500"

    def test_milliseconds_round_up_carries_to_seconds(self):
        # 0.9999 * 1000 = 999.9 → round → 1000ms → carry to 1.000s
        assert _format_timecode(0.9999) == "00:00:01,000"

    def test_milliseconds_round_down(self):
        assert _format_timecode(0.0004) == "00:00:00,000"


class TestWrap:
    def test_short_text_single_line(self):
        assert _wrap("Hello world") == "Hello world"

    def test_long_text_two_lines(self):
        # ~60 chars → must split into 2 lines, each ≤42
        text = "Today we are going to walk through prompting best practices today"
        result = _wrap(text)
        lines = result.split("\n")
        assert len(lines) == 2
        assert all(len(line) <= 42 for line in lines)

    def test_overflow_truncates_with_ellipsis(self):
        # Very long text → 2 lines, last ends with "…"
        text = "word " * 60  # 300 chars of "word word word..."
        result = _wrap(text)
        lines = result.split("\n")
        assert len(lines) == 2
        assert lines[1].endswith("…")
        assert all(len(line) <= 42 for line in lines)

    def test_exact_two_lines_no_ellipsis(self):
        # Fits exactly in 2 lines without truncation → no ellipsis
        text = "a" * 30 + " " + "b" * 30  # 61 chars, splits 30/30 by space
        result = _wrap(text)
        lines = result.split("\n")
        assert len(lines) == 2
        assert not lines[1].endswith("…")


class TestEscape:
    def test_strips_outer_whitespace(self):
        assert _escape("  hello  ") == "hello"

    def test_collapses_internal_newlines_to_space(self):
        assert _escape("line1\nline2") == "line1 line2"

    def test_collapses_carriage_returns(self):
        assert _escape("line1\r\nline2") == "line1 line2"

    def test_replaces_arrow_sequence(self):
        assert _escape("a-->b") == "a‐‐>b"

    def test_combined(self):
        assert _escape("  a-->b\nc  ") == "a‐‐>b c"


def _seg(start, end, original="", translated=""):
    return Segment(start=start, end=end, original=original, translated=translated)


class TestWriteSrt:
    def test_basic_two_segments_en(self, tmp_path):
        segs = [
            _seg(0.0, 1.5, original="Hello world."),
            _seg(2.0, 4.25, original="This is segment two."),
        ]
        path = tmp_path / "out.en.srt"
        n = write_srt(segs, str(path), lang="en")
        assert n == 2
        expected = (
            "1\n"
            "00:00:00,000 --> 00:00:01,500\n"
            "Hello world.\n"
            "\n"
            "2\n"
            "00:00:02,000 --> 00:00:04,250\n"
            "This is segment two.\n"
            "\n"
        )
        assert path.read_text(encoding="utf-8") == expected

    def test_basic_two_segments_ru(self, tmp_path):
        segs = [
            _seg(0.0, 1.0, original="Hi.", translated="Привет."),
            _seg(1.0, 2.0, original="Bye.", translated="Пока."),
        ]
        path = tmp_path / "out.ru.srt"
        n = write_srt(segs, str(path), lang="ru")
        assert n == 2
        content = path.read_text(encoding="utf-8")
        assert "Привет." in content
        assert "Пока." in content
        assert "Hi." not in content

    def test_returns_cue_count(self, tmp_path):
        segs = [_seg(0.0, 1.0, original="A.")]
        path = tmp_path / "out.en.srt"
        assert write_srt(segs, str(path), lang="en") == 1
