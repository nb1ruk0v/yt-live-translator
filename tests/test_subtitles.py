from subtitles import _format_timecode


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
