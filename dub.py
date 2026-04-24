import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml

from group import group_segments
from merge import merge
from transcribe import transcribe
from translate import translate
from tts import synthesize


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def check_prerequisites(config: dict) -> None:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg not found. Install with: brew install ffmpeg")

    try:
        r = requests.get(f"{config['translation']['ollama_url']}/api/tags", timeout=3)
        r.raise_for_status()
    except Exception as e:
        raise RuntimeError(
            f"Ollama not reachable at {config['translation']['ollama_url']}. Run: ollama serve"
        ) from e


def is_url(s: str) -> bool:
    p = urlparse(s)
    return p.scheme in ("http", "https") and bool(p.netloc)


def download_video(url: str, out_dir: str = "data") -> str:
    if subprocess.run(["which", "yt-dlp"], capture_output=True).returncode != 0:
        raise RuntimeError("yt-dlp not found. Install with: brew install yt-dlp")

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    template = f"{out_dir}/%(title).100B [%(id)s].%(ext)s"
    print(f"Downloading {url} ...")
    result = subprocess.run(
        [
            "yt-dlp",
            "-f",
            "bv*+ba/b",
            "-S",
            "res:720",
            "--merge-output-format",
            "mp4",
            "--print",
            "after_move:filepath",
            "--no-simulate",
            "-o",
            template,
            url,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp failed:\n{result.stderr}")

    path = result.stdout.strip().splitlines()[-1]
    print(f"Saved to: {path}")
    return path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python dub.py <video_file|url>")
        sys.exit(1)

    arg = sys.argv[1]
    if is_url(arg):
        video_path = download_video(arg)
    else:
        video_path = arg
        if not Path(video_path).exists():
            print(f"Error: File not found: {video_path}")
            sys.exit(1)

    config = load_config()

    print("Checking prerequisites...")
    check_prerequisites(config)

    print("[1/4] Transcribing...")
    segments = transcribe(video_path, config["transcription"])
    print(f"      Found {len(segments)} segments")

    grouping = config.get("grouping", {})
    gap = grouping.get("gap_threshold", 0.3)
    max_dur = grouping.get("max_duration", 12.0)
    segments = group_segments(segments, gap_threshold=gap, max_duration=max_dur)
    print(f"      Grouped into {len(segments)} (gap < {gap}s, max {max_dur}s)")

    print("[2/4] Translating...")
    segments = translate(segments, config["translation"])

    print("[3/4] Synthesizing speech...")
    segments = synthesize(segments, config["tts"])

    print("[4/4] Merging audio...")
    output = merge(video_path, segments, config["output"]["suffix"])

    print(f"\nDone! Output saved to: {output}")


if __name__ == "__main__":
    main()
