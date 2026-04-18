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
        # no kyrillic → _clean just strips; caller handles fallback
        assert _clean("  hello world  ") == "hello world"
