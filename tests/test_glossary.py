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
    opts = mock_post.call_args[1]["json"]["options"]
    assert opts["temperature"] == 0
    # full transcript must fit the context and the glossary must not be capped mid-table
    assert opts["num_ctx"] == 16384
    assert opts["num_predict"] == 2048


@patch("glossary.requests.post")
def test_build_glossary_reports_token_counts(mock_post, tmp_path, capsys):
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"message": {"content": MD}, "prompt_eval_count": 4500, "eval_count": 800},
    )
    build_glossary(
        [Segment(start=0.0, end=1.0, original="Test")], FAKE_CONFIG, str(tmp_path / "g.md")
    )
    out = capsys.readouterr().out
    assert "input 4500/16384" in out
    assert "output 800/2048" in out


@patch("glossary.requests.post")
def test_build_glossary_warns_when_output_capped(mock_post, tmp_path, capsys):
    # eval_count == num_predict means the glossary was cut off — must surface a warning
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"message": {"content": MD}, "prompt_eval_count": 100, "eval_count": 2048},
    )
    build_glossary(
        [Segment(start=0.0, end=1.0, original="Test")], FAKE_CONFIG, str(tmp_path / "g.md")
    )
    assert "num_predict cap" in capsys.readouterr().err


def test_build_glossary_empty_segments_returns_empty(tmp_path):
    result = build_glossary([], FAKE_CONFIG, str(tmp_path / "g.md"))
    assert result == ""


def test_build_glossary_blank_originals_returns_empty(tmp_path):
    segments = [Segment(start=0.0, end=1.0, original="   ")]
    result = build_glossary(segments, FAKE_CONFIG, str(tmp_path / "g.md"))
    assert result == ""


@patch("glossary.requests.post")
def test_build_glossary_llm_error_returns_empty(mock_post, tmp_path):
    import requests as _requests

    mock_post.side_effect = _requests.RequestException("boom")
    segments = [Segment(start=0.0, end=1.0, original="Test")]

    result = build_glossary(segments, FAKE_CONFIG, str(tmp_path / "g.md"))

    assert result == ""


@patch("glossary.requests.post")
def test_build_glossary_returns_md_even_if_save_fails(mock_post, tmp_path):
    # LLM succeeded → context is usable in memory; a failed file write must not
    # crash the pipeline and must not discard the context.
    mock_post.return_value = _mock_chat_response(MD)
    segments = [Segment(start=0.0, end=1.0, original="Test")]

    with patch("builtins.open", side_effect=OSError("disk full")):
        result = build_glossary(segments, FAKE_CONFIG, str(tmp_path / "g.md"))

    assert result == MD
