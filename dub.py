import sys
import yaml
import subprocess
import requests
from pathlib import Path

from transcribe import transcribe
from translate import translate
from tts import synthesize
from merge import merge


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def check_prerequisites(config: dict) -> None:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg not found. Install with: brew install ffmpeg")

    try:
        r = requests.get(
            f"{config['translation']['ollama_url']}/api/tags", timeout=3
        )
        r.raise_for_status()
    except Exception as e:
        raise RuntimeError(
            f"Ollama not reachable at {config['translation']['ollama_url']}. "
            "Run: ollama serve"
        ) from e


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python dub.py <video_file>")
        sys.exit(1)

    video_path = sys.argv[1]
    if not Path(video_path).exists():
        print(f"Error: File not found: {video_path}")
        sys.exit(1)

    config = load_config()

    print("Checking prerequisites...")
    check_prerequisites(config)

    print("[1/4] Transcribing...")
    segments = transcribe(video_path, config["transcription"])
    print(f"      Found {len(segments)} segments")

    print("[2/4] Translating...")
    segments = translate(segments, config["translation"])

    print("[3/4] Synthesizing speech...")
    segments = synthesize(segments, config["tts"])

    print("[4/4] Merging audio...")
    output = merge(video_path, segments, config["output"]["suffix"])

    print(f"\nDone! Output saved to: {output}")


if __name__ == "__main__":
    main()
