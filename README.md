# vt-claude — Video Translation & Dubbing

Automatic video dubbing pipeline: transcription → translation → speech synthesis → mux.

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

The first run will additionally download the XTTS-v2 model (~1.8 GB) into the Coqui TTS cache and prompt for interactive consent to the CPML license — answer `y`.

## Pipeline

```
video.mp4 / URL
    │
    ▼
[1] src/transcribe.py   faster-whisper      text + timings (Segment.original)
    │
    ▼
[2] src/translate.py    Ollama /api/chat    translation to RU with N=3 history
    │                                       (Segment.translated)
    ▼
[3] src/tts.py          Coqui XTTS-v2       voice cloning: reference clip
    │                                       extracted from the input video,
    │                                       one WAV per segment
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
2. **`src/tts.py`** — XTTS-v2 synthesizes a WAV (using a reference clip cloned from the
   input video); the actual duration is written into `Segment.audio_duration`. **Known
   regression:** XTTS-v2 on RU is markedly slower than the previous Silero backend — on
   the test video 400/416 segments required `atempo` and 228s were truncated. See done
   item `#10` for the planned mitigation (XTTS `speed` parameter / compaction-rewrite).
3. **`src/merge.py`** — if `audio_duration > seg.duration`:
   - `atempo` with the corresponding ratio, clamped at `ATEMPO_MAX = 1.5`
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

translation:
  model: "gemma4:e4b"
  ollama_url: "http://localhost:11434"

tts:
  model: "tts_models/multilingual/multi-dataset/xtts_v2"
  language: "ru"
  device: "cpu"          # cpu | cuda | mps
  reference_seconds: 10  # length of the reference clip for voice cloning

output:
  suffix: "_dubbed"
```

**Voice:** cloned automatically from the first `reference_seconds` of the input
video (`src/tts.py:_extract_reference`). The reference is saved as
`<video>_ref.wav` next to the source and reused for every segment, so the
Russian track inherits the original speaker's voice. To pin a fixed voice
instead, swap `speaker_wav` in `synthesize` for a custom WAV. F5-TTS as an
alternative backend was tried and shelved on the `experiment/tts-f5` branch.

## Stack

| Component | Tool | Purpose |
|---|---|---|
| Transcription | faster-whisper | Whisper, CPU, `int8` |
| Translation | Ollama (`/api/chat`, `gemma4:e4b`) | Sliding-window history N=3, `temperature=0`, length hint |
| Speech synthesis | Coqui XTTS-v2 (`coqui-tts`) | Voice cloning, multilingual (RU here); reference clip auto-extracted from the input video |
| Mux | ffmpeg / ffmpeg-python | Audio extraction, atempo stretch, amix |
| URL download | yt-dlp | Optional — only when the input is an http(s) URL |

## Remote run

If the pipeline is too slow on your laptop, ship it to a GPU server via
`run_remote.sh`. The script rsyncs the codebase, runs an arbitrary
command over SSH, and pulls `data/` back.

```bash
# one-time: configure the server target
cp .env.example .env           # if not already present
# edit .env and set REMOTE_HOST=user@gpu-host (REMOTE_DIR defaults to ~/vt-claude)

# run tests on the server
./run_remote.sh uv run pytest

# dub a local file (uploads data/ first)
./run_remote.sh --sync-data uv run src/dub.py "data/my_video.mp4"

# dub a URL (yt-dlp runs on the server, nothing to upload)
./run_remote.sh uv run src/dub.py "https://www.youtube.com/watch?v=..."
```

**What the script syncs.** Code goes up via `rsync` with the usual
excludes (`.git/`, `__pycache__/`, `.venv/`, caches, `experiments/`,
`.DS_Store`). `.env` and `config.yaml` are also excluded — the server
holds its own copies (typically with `device: cuda` in `config.yaml`
and `HUGGINGFACE_TOKEN` in `.env`). `data/` only goes up with
`--sync-data`. After the remote command finishes successfully, the
script pulls `data/` back incrementally.

**Server pre-requisites (one-time).**

- `uv` and `ffmpeg` in `PATH`
- `ollama serve` + `ollama pull gemma4:e4b`
- NVIDIA driver and CUDA toolkit for `torch`
- `git clone` this repo into `$REMOTE_DIR`, `uv sync`
- copy `.env.example` to `.env` on the server, set `HUGGINGFACE_TOKEN`
- copy `config.yaml` to the server and set `tts.device` / `transcription.device` to `cuda`

**Recovery.** If the remote command fails, `data/` is not pulled back.
Run `./run_remote.sh true` (or any no-op) to trigger only the
download phase against the current server state.

## Tests

```bash
uv run pytest
```

Unit tests cover `translate` (including `_clean`, history, fallback),
`merge`, `tts`, `transcribe`, `dub`, `segment`.
