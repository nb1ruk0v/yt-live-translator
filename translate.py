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
