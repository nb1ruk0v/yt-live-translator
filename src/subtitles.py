"""Sidecar SRT subtitle writer.

Spec: docs/superpowers/specs/2026-05-03-srt-subtitles-design.md
"""


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
