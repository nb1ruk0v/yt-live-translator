"""Sidecar SRT subtitle writer.

Spec: docs/superpowers/specs/2026-05-03-srt-subtitles-design.md
"""

import textwrap
from typing import Literal

from segment import Segment


def _format_timecode(seconds: float) -> str:
    """Format seconds as 'HH:MM:SS,mmm' (SRT timecode, comma decimal)."""
    total_ms = round(seconds * 1000)
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _wrap(text: str, width: int = 42, max_lines: int = 2) -> str:
    """Wrap text into at most `max_lines` of `width` chars; truncate with '…' if overflow."""
    lines = textwrap.wrap(text, width=width)
    if len(lines) <= max_lines:
        return "\n".join(lines)
    kept = lines[:max_lines]
    # Trim last line to fit width including ellipsis
    last = kept[-1]
    if len(last) + 1 > width:
        last = last[: width - 1].rstrip()
    kept[-1] = last + "…"
    return "\n".join(kept)


def _escape(text: str) -> str:
    """Strip whitespace, collapse internal newlines to space, neutralize '-->' sequence."""
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ")
    text = text.replace("-->", "‐‐>")  # en-dash chars, not hyphen-minus
    return text.strip()


def write_srt(segments: list[Segment], path: str, lang: Literal["en", "ru"]) -> int:
    """Write `segments` as SRT to `path`. Returns count of cues written.

    `lang="en"` uses seg.original; `lang="ru"` uses seg.translated.
    Existing files at `path` are overwritten.
    """
    count = 0
    with open(path, "w", encoding="utf-8") as f:
        for seg in segments:
            text = seg.original if lang == "en" else seg.translated
            text = _escape(text)
            text = _wrap(text)
            count += 1
            f.write(f"{count}\n")
            f.write(f"{_format_timecode(seg.start)} --> {_format_timecode(seg.end)}\n")
            f.write(f"{text}\n\n")
    return count
