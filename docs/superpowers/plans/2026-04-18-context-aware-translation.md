# Context-Aware Translation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `translate.py` to translate Whisper segments via Ollama `/api/chat` with sliding-window history (N=3), deterministic sampling, and response post-processing.

**Architecture:** Single module `translate.py` with public `translate(segments, config)` preserving signature. Adds private helpers: `_clean(text)` for LLM-response sanitization, `_build_messages(seg, history)` for chat-message assembly. Per-call state is a local `history: list[tuple[str, str]]` sliced with `[-3:]`.

**Tech Stack:** Python 3.11, `requests`, Ollama `/api/chat` endpoint, pytest + unittest.mock.

---

## File Structure

- **Modify:** `translate.py` — full rewrite.
- **Modify:** `tests/test_translate.py` — rewrite existing tests against new `/api/chat` contract, add tests for `_clean` and history/context behavior.
- **No changes:** `segment.py`, `config.yaml`, `transcribe.py`, `tts.py`, `merge.py`, `dub.py`.

Spec: `docs/superpowers/specs/2026-04-18-context-aware-translation-design.md`.

---

## Task 1: Implement `_clean` post-processor (TDD)

**Files:**
- Modify: `translate.py`
- Test: `tests/test_translate.py`

- [ ] **Step 1: Replace test file with `_clean` tests first**

Overwrite `tests/test_translate.py` with this starting content (existing tests will be re-added in later tasks):

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_translate.py -v`
Expected: ImportError / AttributeError — `_clean` not defined.

- [ ] **Step 3: Implement `_clean` in `translate.py`**

Overwrite `translate.py` with:

```python
import re
import requests
from segment import Segment

SYSTEM_PROMPT = (
    "You are a professional subtitle translator. "
    "Translate the user's text to natural, fluent Russian. "
    "Preserve meaning, tone and proper nouns. "
    "Output ONLY the Russian translation — no quotes, no prefixes, "
    "no explanations, no notes, no English."
)

CONTEXT_WINDOW = 3
CYRILLIC_RE = re.compile(r"[а-яА-ЯёЁ]")


def _clean(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    # strip matching outer quotes (ascii + guillemets)
    for q_open, q_close in (('"', '"'), ("'", "'"), ("«", "»")):
        if text.startswith(q_open) and text.endswith(q_close) and len(text) >= 2:
            text = text[len(q_open):-len(q_close)].strip()
    # if multi-line, pick first non-empty line that contains cyrillic
    if "\n" in text:
        for line in (ln.strip() for ln in text.split("\n")):
            if line and CYRILLIC_RE.search(line):
                return line
        # no cyrillic line → fall through to stripped full text
        return text.strip()
    return text


def translate(segments: list[Segment], config: dict) -> list[Segment]:
    # full implementation added in Task 2
    raise NotImplementedError
```

- [ ] **Step 4: Run `_clean` tests to verify they pass**

Run: `uv run pytest tests/test_translate.py -v -k TestClean`
Expected: all 8 TestClean tests PASS.

- [ ] **Step 5: Commit**

```bash
git add translate.py tests/test_translate.py
git commit -m "feat(translate): add _clean post-processor with tests"
```

---

## Task 2: Implement `translate` with `/api/chat` and N=3 history (TDD)

**Files:**
- Modify: `translate.py`
- Test: `tests/test_translate.py`

- [ ] **Step 1: Append integration tests for `translate` to `tests/test_translate.py`**

Append these tests (to the end of the existing file, outside `TestClean`):

```python
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
    responses = iter([
        _mock_chat_response("Один"),
        _mock_chat_response("Два"),
        _mock_chat_response("Три"),
        _mock_chat_response("Четыре"),
        _mock_chat_response("Пять"),
    ])
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_translate.py -v`
Expected: TestClean tests still pass; all new tests FAIL with `NotImplementedError`.

- [ ] **Step 3: Replace `translate` body with real implementation**

In `translate.py`, replace the `translate` function (keep imports, constants, and `_clean` untouched):

```python
import sys


def _build_messages(
    seg_original: str, history: list[tuple[str, str]]
) -> list[dict]:
    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for orig, trans in history:
        messages.append({"role": "user", "content": orig})
        messages.append({"role": "assistant", "content": trans})
    messages.append({"role": "user", "content": seg_original})
    return messages


def translate(segments: list[Segment], config: dict) -> list[Segment]:
    history: list[tuple[str, str]] = []

    for seg in segments:
        if not seg.original.strip():
            seg.translated = ""
            continue

        messages = _build_messages(seg.original, history[-CONTEXT_WINDOW:])
        response = requests.post(
            f"{config['ollama_url']}/api/chat",
            json={
                "model": config["model"],
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0},
            },
            timeout=120,
        )
        response.raise_for_status()
        raw = response.json()["message"]["content"]
        cleaned = _clean(raw)

        if not cleaned or not CYRILLIC_RE.search(cleaned):
            print(
                f"[translate] warning: invalid LLM response for segment "
                f"{seg.start:.2f}-{seg.end:.2f}, falling back to original",
                file=sys.stderr,
            )
            cleaned = seg.original

        seg.translated = cleaned
        history.append((seg.original, cleaned))

    return segments
```

Note: move `import sys` to the top of the file with the other imports.

- [ ] **Step 4: Run full test file to verify all tests pass**

Run: `uv run pytest tests/test_translate.py -v`
Expected: all tests PASS (8 TestClean + 13 translate tests = 21 total).

- [ ] **Step 5: Commit**

```bash
git add translate.py tests/test_translate.py
git commit -m "feat(translate): context-aware chat with N=3 history and fallback"
```

---

## Task 3: Smoke-test end-to-end pipeline

**Files:** none modified.

- [ ] **Step 1: Verify Ollama is running**

Run: `curl -s http://localhost:11434/api/tags | head -c 200`
Expected: JSON with models list. If fails → user must run `ollama serve`; stop and report.

- [ ] **Step 2: Run full pipeline on test video**

Run: `uv run dub.py data/test_video.mp4`
Expected: prints `[1/4]` through `[4/4]` without errors, final message `Done! Output saved to: data/test_video_dubbed.mp4`.

- [ ] **Step 3: Verify output file exists**

Run: `ls -la data/test_video_dubbed.mp4`
Expected: file exists, size > 0.

- [ ] **Step 4: Report qualitative check to user**

Report: pipeline ran end-to-end. Ask user to watch the dubbed video and compare translation quality against previous runs (especially pronoun/term consistency across adjacent segments). Do NOT claim quality improvement without user confirmation — we only verified non-crash, not translation quality.

No commit — this task is verification only.

---

## Self-review notes

- Spec coverage: system prompt ✓ (Task 1 impl), N=3 history ✓ (Task 2 tests + impl), temperature=0 ✓, post-processing ✓ (Task 1 tests), empty-original skip ✓, non-cyrillic fallback ✓, timeout 120s ✓, `/api/chat` ✓.
- Types/names consistent: `CONTEXT_WINDOW`, `CYRILLIC_RE`, `SYSTEM_PROMPT`, `_clean`, `_build_messages` used with same signatures in every task.
- No placeholders, no "similar to" references, no vague "add error handling".
