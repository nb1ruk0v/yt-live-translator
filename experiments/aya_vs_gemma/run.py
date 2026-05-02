"""A/B-сравнение моделей перевода gemma4:e4b vs aya-expanse:8b.

Spec: docs/superpowers/specs/2026-05-03-aya-vs-gemma-design.md
"""

import argparse
import sys
from pathlib import Path

import requests
import yaml

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


def load_config() -> dict:
    with open(ROOT / "config.yaml") as f:
        return yaml.safe_load(f)


def check_ollama_models(ollama_url: str, required: list[str]) -> None:
    r = requests.get(f"{ollama_url}/api/tags", timeout=5)
    r.raise_for_status()
    available = {m["name"] for m in r.json().get("models", [])}
    missing = [m for m in required if m not in available]
    if missing:
        raise RuntimeError(
            f"Missing Ollama models: {missing}. Pull with: "
            + " && ".join(f"ollama pull {m}" for m in missing)
        )


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
    cfg = load_config()
    check_ollama_models(cfg["translation"]["ollama_url"], list(MODEL_TAGS))
    print(f"[ab] videos: {videos}")
    print(f"[ab] skip_audio: {args.skip_audio}")
    print(f"[ab] models OK: {list(MODEL_TAGS)}")


if __name__ == "__main__":
    main()
