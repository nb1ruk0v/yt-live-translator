"""A/B-сравнение моделей перевода gemma4:e4b vs aya-expanse:8b.

Spec: docs/superpowers/specs/2026-05-03-aya-vs-gemma-design.md
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
HERE = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "src"))

VIDEOS = [
    "From Vibe Coding to Agentic Engineering.mp4",
    "Mastering Claude Code in 30 minutes.mp4",
    "Prompting for Agents.mp4",
]

MODEL_TAGS = {
    "gemma4:e4b": "gemma",
    "aya-expanse:8b": "aya",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--skip-audio",
        action="store_true",
        help="Skip TTS+merge, only produce translations.md (fast smoke mode).",
    )
    p.add_argument(
        "videos",
        nargs="*",
        help="Optional subset of video filenames (default: all 3 in VIDEOS).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    videos = args.videos or VIDEOS
    print(f"[ab] videos: {videos}")
    print(f"[ab] skip_audio: {args.skip_audio}")
    print(f"[ab] models: {list(MODEL_TAGS)}")


if __name__ == "__main__":
    main()
