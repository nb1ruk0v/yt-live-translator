from unittest.mock import patch, MagicMock
from segment import Segment
from translate import translate


FAKE_CONFIG = {
    "model": "llama3.2:3b",
    "ollama_url": "http://localhost:11434",
}


def make_segments():
    return [
        Segment(start=0.0, end=2.0, original="Hello world"),
        Segment(start=2.5, end=5.0, original="How are you"),
    ]


@patch("translate.requests.post")
def test_translate_fills_translated(mock_post):
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"response": "  Привет мир  "},
    )

    segments = make_segments()
    result = translate(segments, FAKE_CONFIG)

    assert result[0].translated == "Привет мир"
    assert mock_post.call_count == 2


@patch("translate.requests.post")
def test_translate_uses_config_model(mock_post):
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"response": "Текст"},
    )

    segments = [Segment(start=0.0, end=1.0, original="Test")]
    translate(segments, {**FAKE_CONFIG, "model": "mistral:7b"})

    call_json = mock_post.call_args[1]["json"]
    assert call_json["model"] == "mistral:7b"


@patch("translate.requests.post")
def test_translate_prompt_contains_original(mock_post):
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"response": "Тест"},
    )

    segments = [Segment(start=0.0, end=1.0, original="Unique phrase XYZ")]
    translate(segments, FAKE_CONFIG)

    call_json = mock_post.call_args[1]["json"]
    assert "Unique phrase XYZ" in call_json["prompt"]


@patch("translate.requests.post")
def test_translate_returns_same_list(mock_post):
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"response": "Привет"},
    )

    segments = make_segments()
    result = translate(segments, FAKE_CONFIG)

    assert result is segments
