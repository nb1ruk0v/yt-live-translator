import sys

import requests

from segment import Segment

SYSTEM_PROMPT = (
    "You are a translation assistant preparing context for dubbing an English "
    "video into Russian. Given the full transcript, produce a SHORT briefing in "
    "Markdown with exactly two sections:\n\n"
    "# Summary\n2-3 sentences (in Russian) describing the topic of the video.\n\n"
    "# Glossary\nA Markdown table with columns | Термин | Перевод/транслит |. "
    "Include company names, product/brand names and technical terms. For each, "
    "give the consistent Russian rendering to use throughout (transliterate "
    "brand/proper names to Cyrillic, e.g. OpenAI → ОупенЭйАй, GPT → Джи-Пи-Ти). "
    "Only include terms that actually appear in the transcript.\n\n"
    "Output ONLY the Markdown, no preamble, no code fences."
)


def build_glossary(segments: list[Segment], config: dict, out_path: str) -> str:
    text = "\n".join(s.original.strip() for s in segments if s.original.strip())
    if not text:
        return ""

    try:
        response = requests.post(
            f"{config['ollama_url']}/api/chat",
            json={
                "model": config["model"],
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                "stream": False,
                "options": {"temperature": 0, "num_predict": 1024},
            },
            timeout=600,
        )
        response.raise_for_status()
        md = response.json()["message"]["content"].strip()
    except Exception as e:  # noqa: BLE001 — pipeline must not die on glossary
        print(
            f"[glossary] warning: build failed ({e}); continuing without context", file=sys.stderr
        )
        return ""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    return md
