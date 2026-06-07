from unittest.mock import MagicMock, patch

from glossary import build_glossary
from segment import Segment

FAKE_CONFIG = {
    "model": "gemma4:e4b",
    "ollama_url": "http://localhost:11434",
}

MD = "# Summary\nПро ИИ.\n\n# Glossary\n| Термин | Перевод |\n|---|---|\n| GPT | Джи-Пи-Ти |"


def _mock_chat_response(content: str) -> MagicMock:
    return MagicMock(status_code=200, json=lambda: {"message": {"content": content}})


@patch("glossary.requests.post")
def test_build_glossary_returns_markdown_and_writes_file(mock_post, tmp_path):
    mock_post.return_value = _mock_chat_response(MD)
    segments = [
        Segment(start=0.0, end=2.0, original="GPT is a model"),
        Segment(start=2.0, end=4.0, original="It is made by OpenAI"),
    ]
    out = tmp_path / "vid_glossary.md"

    result = build_glossary(segments, FAKE_CONFIG, str(out))

    assert result == MD
    assert out.read_text() == MD


@patch("glossary.requests.post")
def test_build_glossary_prompt_contains_all_originals(mock_post, tmp_path):
    mock_post.return_value = _mock_chat_response(MD)
    segments = [
        Segment(start=0.0, end=2.0, original="Alpha phrase"),
        Segment(start=2.0, end=4.0, original="Beta phrase"),
    ]

    build_glossary(segments, FAKE_CONFIG, str(tmp_path / "g.md"))

    sent = mock_post.call_args[1]["json"]
    blob = " ".join(m["content"] for m in sent["messages"])
    assert "Alpha phrase" in blob
    assert "Beta phrase" in blob


@patch("glossary.requests.post")
def test_build_glossary_hits_chat_endpoint_with_config_model(mock_post, tmp_path):
    mock_post.return_value = _mock_chat_response(MD)
    segments = [Segment(start=0.0, end=1.0, original="Test")]

    build_glossary(segments, {**FAKE_CONFIG, "model": "mistral:7b"}, str(tmp_path / "g.md"))

    assert mock_post.call_args[0][0].endswith("/api/chat")
    assert mock_post.call_args[1]["json"]["model"] == "mistral:7b"
    assert mock_post.call_args[1]["json"]["options"]["temperature"] == 0
