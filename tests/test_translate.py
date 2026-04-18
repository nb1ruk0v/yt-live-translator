import pytest
import requests
from unittest.mock import patch, MagicMock
from segment import Segment
from translate import translate, _clean


class TestClean:
    def test_strips_whitespace(self):
        assert _clean("  Привет мир  ") == "Привет мир"

    def test_strips_ascii_quotes(self):
        assert _clean('"Привет мир"') == "Привет мир"
        assert _clean("'Привет мир'") == "Привет мир"

    def test_strips_guillemets(self):
        assert _clean("«Привет мир»") == "Привет мир"

    def test_strips_stacked_quotes(self):
        # current behavior: loop strips multiple layers in one call.
        # pin this so Task 2 (which makes _clean load-bearing) can't drift silently.
        assert _clean("'«Привет мир»'") == "Привет мир"

    def test_picks_first_cyrillic_line_after_prefix(self):
        raw = "Here's the translation:\nПривет мир"
        assert _clean(raw) == "Привет мир"

    def test_multiline_picks_first_cyrillic(self):
        raw = "Note: informal register\n\nПривет, как дела?\n\n(optional)"
        assert _clean(raw) == "Привет, как дела?"

    def test_empty_string(self):
        assert _clean("") == ""

    def test_only_whitespace(self):
        assert _clean("   \n  ") == ""

    def test_no_cyrillic_returns_stripped(self):
        # no cyrillic → _clean just strips; caller handles fallback
        assert _clean("  hello world  ") == "hello world"

    def test_multiline_no_cyrillic_returns_stripped_full(self):
        # dead branch otherwise; pin fallback behavior
        assert _clean("  Hello\nWorld  ") == "Hello\nWorld"
