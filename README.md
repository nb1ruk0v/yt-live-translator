# vt-claude — Video Translation & Dubbing

Automatic video dubbing pipeline: transcription → grouping → translation → speech synthesis → mux.

## Quick start

```bash
# local file
uv run src/dub.py data/test_video.mp4

# or URL (YouTube etc., via yt-dlp)
uv run src/dub.py "https://www.youtube.com/watch?v=..."
```

The output is written next to the source with a `_dubbed` suffix:
`data/test_video_dubbed.mp4`. For URL inputs the video is first downloaded into `data/`.

## Installation

**Requirements:** Python 3.11, [uv](https://github.com/astral-sh/uv), ffmpeg,
[Ollama](https://ollama.ai). For URL inputs, additionally `yt-dlp`.

```bash
# dependencies
uv sync

# system tools
brew install ffmpeg
brew install yt-dlp      # only if you plan to feed URLs

# LLM for translation
ollama pull gemma4:e4b
ollama serve
```

The first run will additionally download the Silero model (~60 MB) into the `torch.hub` cache.

## Pipeline

```
video.mp4 / URL
    │
    ▼
[1] src/transcribe.py   faster-whisper      text + timings (Segment.original)
    │
    ▼
    src/group.py        gap-based merge     short segments are merged
    │                                       (with max_duration cap)
    ▼
[2] src/translate.py    Ollama /api/chat    translation to RU with N=3 history
    │                                       (Segment.translated)
    ▼
[3] src/tts.py          Silero (v4_ru)      one WAV per segment
    │                                       (Segment.audio_path/audio_duration)
    ▼
[4] src/merge.py        ffmpeg-python       atempo stretch + atrim cap,
                                            amix on top of the video
    ▼
video_dubbed.mp4
```

The central object is `Segment` (`src/segment.py`): `start`, `end`, `original`,
`translated`, `audio_path`, `audio_duration`.

## Dubbing synchronization

Russian translation is typically 20–50% longer than the original, so:

1. **`src/translate.py`** — a length hint is added to the system prompt
   (`Keep the translation close to N characters`) so the LLM does not inflate the length itself.
2. **`src/tts.py`** — Silero synthesizes a WAV; the actual duration is written into
   `Segment.audio_duration`.
3. **`src/merge.py`** — if `audio_duration > seg.duration`:
   - `atempo` with the corresponding ratio, clamped at `ATEMPO_MAX = 1.25`
     (preserves pitch, speeds up the speech);
   - `atrim(duration=seg.duration)` as a safety cap — without it the tail bleeds
     into the next window and gets mixed by `amix` as a "second voice".
4. If `audio_duration ≤ seg.duration` — no filters are applied,
   the rest of the window stays silent.

`src/merge.py` prints per-segment diagnostics (`atempo=…, truncated …s`)
and a final line indicating how many segments were stretched.

## Configuration

All parameters live in `config.yaml`:

```yaml
transcription:
  model: "base"          # tiny / base / small / medium / large
  device: "cpu"          # cpu | cuda | mps
  language: "auto"       # auto = autodetect, or "en", "ru", etc.

grouping:
  gap_threshold: 0.3     # seconds — segments with a smaller gap are merged
  max_duration: 12.0     # seconds — upper bound on merged segment duration

translation:
  model: "gemma4:e4b"
  ollama_url: "http://localhost:11434"

tts:
  model: "v4_ru"         # Silero RU bundle
  language: "ru"
  speaker: "eugene"      # aidar | eugene | baya | kseniya | xenia
  sample_rate: 48000

output:
  suffix: "_dubbed"
```

**Changing the voice:** swap `speaker` in `config.yaml`. Silero does not support
voice cloning — if you need that, look at F5-TTS / XTTS.

## Stack

| Component | Tool | Purpose |
|---|---|---|
| Transcription | faster-whisper | Whisper, CPU, `int8` |
| Grouping | `src/group.py` | Merges short Whisper segments by `gap_threshold`, capped by `max_duration` |
| Translation | Ollama (`/api/chat`, `gemma4:e4b`) | Sliding-window history N=3, `temperature=0`, length hint |
| Speech synthesis | Silero TTS (`v4_ru`) | RU, loaded via `torch.hub` from `snakers4/silero-models` |
| Mux | ffmpeg / ffmpeg-python | Audio extraction, atempo stretch, amix |
| URL download | yt-dlp | Optional — only when the input is an http(s) URL |

## Tests

```bash
uv run pytest
```

Unit tests cover `translate` (including `_clean`, history, fallback),
`group`, `merge`, `tts`, `transcribe`, `dub`, `segment`.
