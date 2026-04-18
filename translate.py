import re
import sys
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
