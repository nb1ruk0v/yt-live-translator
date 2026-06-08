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

# A full transcript (~5k tokens for a 20-min talk) overflows Ollama's default 4k
# context, so the model never sees the end and the glossary gets cut off mid-table.
# 16k leaves generous headroom; num_predict bounds the output so it can't run away.
NUM_CTX = 16384
NUM_PREDICT = 2048


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
                "options": {"temperature": 0, "num_ctx": NUM_CTX, "num_predict": NUM_PREDICT},
            },
            timeout=600,
        )
        response.raise_for_status()
        data = response.json()
        md = data["message"]["content"].strip()
    except Exception as e:  # noqa: BLE001 — pipeline must not die on glossary
        print(
            f"[glossary] warning: build failed ({e}); continuing without context", file=sys.stderr
        )
        return ""

    # Token accounting so transcript/glossary overflow can't slip by unnoticed.
    in_tok = data.get("prompt_eval_count")
    out_tok = data.get("eval_count")
    print(f"[glossary] tokens: input {in_tok}/{NUM_CTX}, output {out_tok}/{NUM_PREDICT}")
    if out_tok is not None and out_tok >= NUM_PREDICT:
        print(
            "[glossary] WARNING: output hit num_predict cap — glossary likely truncated",
            file=sys.stderr,
        )
    if in_tok is not None and in_tok >= NUM_CTX:
        print(
            "[glossary] WARNING: input filled num_ctx — transcript likely truncated",
            file=sys.stderr,
        )

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
    except OSError as e:
        # Saving the .md is best-effort; the context is still usable in memory.
        print(f"[glossary] warning: could not save {out_path} ({e})", file=sys.stderr)
    return md
