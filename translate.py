import requests
from segment import Segment


def translate(segments: list[Segment], config: dict) -> list[Segment]:
    for seg in segments:
        response = requests.post(
            f"{config['ollama_url']}/api/generate",
            json={
                "model": config["model"],
                "prompt": (
                    "Translate the following text to Russian. "
                    "Return only the translation, no explanations:\n\n"
                    f"{seg.original}"
                ),
                "stream": False,
            },
        )
        response.raise_for_status()
        seg.translated = response.json()["response"].strip()
    return segments
