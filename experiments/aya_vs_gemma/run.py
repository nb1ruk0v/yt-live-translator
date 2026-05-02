"""A/B-сравнение моделей перевода gemma4:e4b vs aya-expanse:8b.

Spec: docs/superpowers/specs/2026-05-03-aya-vs-gemma-design.md
"""

import argparse
import sys
from copy import deepcopy
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
HERE = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "src"))

# from src/
from group import group_segments  # noqa: E402
from transcribe import transcribe  # noqa: E402
from translate import translate  # noqa: E402

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


def format_time(seconds: float) -> str:
    """`MM:SS.ms` для коротких видео, `HH:MM:SS.ms` для длинных."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = seconds % 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{sec:06.3f}"
    return f"{minutes:02d}:{sec:06.3f}"


def format_translations_md(
    video_name: str,
    gemma_segs: list,  # list[Segment]
    aya_segs: list,  # list[Segment]
) -> str:
    assert len(gemma_segs) == len(aya_segs), "segment count mismatch"
    lines = [f"# {video_name}", ""]
    for g, a in zip(gemma_segs, aya_segs):
        assert g.start == a.start and g.end == a.end, "timing drift between models"
        lines.append(f"## [{format_time(g.start)} → {format_time(g.end)}] dur={g.duration:.2f}s")
        lines.append("")
        lines.append(f"**EN:** {g.original}")
        lines.append(f"**gemma:** {g.translated}")
        lines.append(f"**aya:** {a.translated}")
        lines.append("")
    return "\n".join(lines)


def process_video(video_name: str, cfg: dict, skip_audio: bool) -> None:
    video_path = DATA / video_name
    if not video_path.exists():
        raise FileNotFoundError(video_path)

    print(f"\n[ab] === {video_name} ===")

    print("[ab] [1/3] transcribe + group (once)")
    base = transcribe(str(video_path), cfg["transcription"])
    grouping = cfg.get("grouping", {})
    base = group_segments(
        base,
        gap_threshold=grouping.get("gap_threshold", 0.3),
        max_duration=grouping.get("max_duration", 12.0),
    )
    print(f"[ab]      base segments: {len(base)}")

    per_model: dict[str, list] = {}
    for model_name, tag in MODEL_TAGS.items():
        print(f"[ab] [2/3] translate ({model_name})")
        segs = deepcopy(base)
        translate(segs, {**cfg["translation"], "model": model_name})
        per_model[tag] = segs

    md_path = HERE / f"{Path(video_name).stem}_translations.md"
    md_path.write_text(format_translations_md(video_name, per_model["gemma"], per_model["aya"]))
    print(f"[ab]      wrote {md_path.relative_to(ROOT)}")

    if skip_audio:
        print("[ab] [3/3] skipped (--skip-audio)")
        return

    # TTS+merge will be added in Task 6
    raise NotImplementedError("audio path will be added in Task 6")


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

    assert format_time(75.5) == "01:15.500", f"format_time bug: {format_time(75.5)}"
    assert format_time(3725.5) == "01:02:05.500", f"format_time bug: {format_time(3725.5)}"

    print(f"[ab] videos: {videos}")
    print(f"[ab] skip_audio: {args.skip_audio}")

    for v in videos:
        process_video(v, cfg, skip_audio=args.skip_audio)

    audio_count = 0 if args.skip_audio else len(videos) * 2
    print(f"\n[ab] done. translations: {len(videos)}, audio: {audio_count}")


if __name__ == "__main__":
    main()
