from unittest.mock import MagicMock, patch

import pytest
import requests

from segment import Segment
from translate import _clean, translate


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


FAKE_CONFIG = {
    "model": "llama3.1:8b",
    "ollama_url": "http://localhost:11434",
}


def _mock_chat_response(content: str) -> MagicMock:
    return MagicMock(
        status_code=200,
        json=lambda: {"message": {"content": content}},
    )


@patch("translate.requests.post")
def test_translate_fills_translated_and_strips(mock_post):
    mock_post.return_value = _mock_chat_response("  Привет мир  ")
    segments = [
        Segment(start=0.0, end=2.0, original="Hello world"),
        Segment(start=2.5, end=5.0, original="How are you"),
    ]

    result = translate(segments, FAKE_CONFIG)

    assert result[0].translated == "Привет мир"
    assert result[1].translated == "Привет мир"
    assert mock_post.call_count == 2


@patch("translate.requests.post")
def test_translate_hits_chat_endpoint(mock_post):
    mock_post.return_value = _mock_chat_response("Текст")
    segments = [Segment(start=0.0, end=1.0, original="Test")]

    translate(segments, FAKE_CONFIG)

    url = mock_post.call_args[0][0]
    assert url.endswith("/api/chat")


@patch("translate.requests.post")
def test_translate_uses_config_model(mock_post):
    mock_post.return_value = _mock_chat_response("Текст")
    segments = [Segment(start=0.0, end=1.0, original="Test")]

    translate(segments, {**FAKE_CONFIG, "model": "mistral:7b"})

    call_json = mock_post.call_args[1]["json"]
    assert call_json["model"] == "mistral:7b"


@patch("translate.requests.post")
def test_translate_sends_system_prompt_and_user_message(mock_post):
    mock_post.return_value = _mock_chat_response("Тест")
    segments = [Segment(start=0.0, end=1.0, original="Unique phrase XYZ")]

    translate(segments, FAKE_CONFIG)

    msgs = mock_post.call_args[1]["json"]["messages"]
    assert msgs[0]["role"] == "system"
    assert msgs[-1]["role"] == "user"
    assert msgs[-1]["content"] == "Unique phrase XYZ"


@patch("translate.requests.post")
def test_translate_sets_temperature_zero(mock_post):
    mock_post.return_value = _mock_chat_response("Тест")
    segments = [Segment(start=0.0, end=1.0, original="Test")]

    translate(segments, FAKE_CONFIG)

    call_json = mock_post.call_args[1]["json"]
    assert call_json["options"]["temperature"] == 0


@patch("translate.requests.post")
def test_translate_disables_stream(mock_post):
    mock_post.return_value = _mock_chat_response("Тест")
    segments = [Segment(start=0.0, end=1.0, original="Test")]

    translate(segments, FAKE_CONFIG)

    assert mock_post.call_args[1]["json"]["stream"] is False


@patch("translate.requests.post")
def test_translate_includes_recent_history_up_to_n3(mock_post):
    # returns unique responses so we can inspect history
    responses = iter(
        [
            _mock_chat_response("Один"),
            _mock_chat_response("Два"),
            _mock_chat_response("Три"),
            _mock_chat_response("Четыре"),
            _mock_chat_response("Пять"),
        ]
    )
    mock_post.side_effect = lambda *a, **kw: next(responses)

    segments = [
        Segment(start=0, end=1, original="One"),
        Segment(start=1, end=2, original="Two"),
        Segment(start=2, end=3, original="Three"),
        Segment(start=3, end=4, original="Four"),
        Segment(start=4, end=5, original="Five"),
    ]
    translate(segments, FAKE_CONFIG)

    # 5th call: history must include last 3 (Two/Два, Three/Три, Four/Четыре)
    last_msgs = mock_post.call_args_list[4][1]["json"]["messages"]
    # system + 3*(user+assistant) + current user = 1 + 6 + 1 = 8
    assert len(last_msgs) == 8
    assert last_msgs[0]["role"] == "system"
    assert last_msgs[1] == {"role": "user", "content": "Two"}
    assert last_msgs[2] == {"role": "assistant", "content": "Два"}
    assert last_msgs[3] == {"role": "user", "content": "Three"}
    assert last_msgs[4] == {"role": "assistant", "content": "Три"}
    assert last_msgs[5] == {"role": "user", "content": "Four"}
    assert last_msgs[6] == {"role": "assistant", "content": "Четыре"}
    assert last_msgs[7] == {"role": "user", "content": "Five"}


@patch("translate.requests.post")
def test_translate_first_segment_has_no_history(mock_post):
    mock_post.return_value = _mock_chat_response("Привет")
    segments = [Segment(start=0, end=1, original="Hello")]

    translate(segments, FAKE_CONFIG)

    msgs = mock_post.call_args[1]["json"]["messages"]
    # system + current user only
    assert len(msgs) == 2


@patch("translate.requests.post")
def test_translate_empty_original_skipped(mock_post):
    mock_post.return_value = _mock_chat_response("Привет")
    segments = [
        Segment(start=0, end=1, original=""),
        Segment(start=1, end=2, original="   "),
        Segment(start=2, end=3, original="Hello"),
    ]

    result = translate(segments, FAKE_CONFIG)

    assert result[0].translated == ""
    assert result[1].translated == ""
    assert result[2].translated == "Привет"
    assert mock_post.call_count == 1


@patch("translate.requests.post")
def test_translate_empty_segments_not_added_to_history(mock_post):
    responses = iter(
        [
            _mock_chat_response("Привет"),
            _mock_chat_response("Пока"),
        ]
    )
    mock_post.side_effect = lambda *a, **kw: next(responses)

    segments = [
        Segment(start=0, end=1, original="Hello"),
        Segment(start=1, end=2, original=""),
        Segment(start=2, end=3, original="   "),
        Segment(start=3, end=4, original="Bye"),
    ]
    translate(segments, FAKE_CONFIG)

    # Second call (for "Bye") should see history of exactly 1 pair (Hello/Привет),
    # NOT the skipped empty segments.
    last_msgs = mock_post.call_args_list[1][1]["json"]["messages"]
    # system + 1 pair (user+assistant) + current user = 4
    assert len(last_msgs) == 4
    assert last_msgs[1] == {"role": "user", "content": "Hello"}
    assert last_msgs[2] == {"role": "assistant", "content": "Привет"}
    assert last_msgs[3] == {"role": "user", "content": "Bye"}


@patch("translate.requests.post")
def test_translate_falls_back_to_original_on_non_cyrillic_response(mock_post):
    mock_post.return_value = _mock_chat_response("I cannot translate this.")
    segments = [Segment(start=0, end=1, original="Mystery text")]

    result = translate(segments, FAKE_CONFIG)

    assert result[0].translated == "Mystery text"


@patch("translate.requests.post")
def test_translate_falls_back_on_empty_response(mock_post):
    mock_post.return_value = _mock_chat_response("")
    segments = [Segment(start=0, end=1, original="Hello")]

    result = translate(segments, FAKE_CONFIG)

    assert result[0].translated == "Hello"


@patch("translate.requests.post")
def test_system_prompt_includes_target_chars(mock_post):
    mock_post.return_value = _mock_chat_response("Тест")
    segments = [Segment(start=0.0, end=1.0, original="Hello world example")]  # 19 chars

    translate(segments, FAKE_CONFIG)

    system = mock_post.call_args[1]["json"]["messages"][0]["content"]
    assert "19" in system


@patch("translate.requests.post")
def test_system_prompt_target_varies_per_segment(mock_post):
    responses = iter([_mock_chat_response("А"), _mock_chat_response("Б")])
    mock_post.side_effect = lambda *a, **kw: next(responses)

    segments = [
        Segment(start=0.0, end=1.0, original="Hi there"),  # 8 chars
        Segment(start=1.0, end=2.0, original="Hello to you!"),  # 13 chars
    ]
    translate(segments, FAKE_CONFIG)

    sys1 = mock_post.call_args_list[0][1]["json"]["messages"][0]["content"]
    sys2 = mock_post.call_args_list[1][1]["json"]["messages"][0]["content"]
    assert "8" in sys1
    assert "13" in sys2


@patch("translate.requests.post")
def test_translate_returns_same_list(mock_post):
    mock_post.return_value = _mock_chat_response("Привет")
    segments = [Segment(start=0.0, end=2.0, original="Hello")]

    result = translate(segments, FAKE_CONFIG)

    assert result is segments


@patch("translate.requests.post")
def test_translate_raises_on_http_error(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500")
    mock_post.return_value = mock_response

    segments = [Segment(start=0.0, end=1.0, original="Test")]
    with pytest.raises(requests.exceptions.HTTPError):
        translate(segments, FAKE_CONFIG)
