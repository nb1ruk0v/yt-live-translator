# vt-claude — Video Translation & Dubbing

Пайплайн автоматического дубляжа видео: транскрипция → группировка → перевод → синтез речи → сборка.

## Быстрый старт

```bash
# локальный файл
uv run dub.py data/test_video.mp4

# или URL (YouTube и пр., через yt-dlp)
uv run dub.py "https://www.youtube.com/watch?v=..."
```

Результат сохраняется рядом с исходником с суффиксом `_dubbed`:
`data/test_video_dubbed.mp4`. Для URL видео сначала скачивается в `data/`.

## Установка

**Требования:** Python 3.11, [uv](https://github.com/astral-sh/uv), ffmpeg,
[Ollama](https://ollama.ai). Для URL-входа дополнительно `yt-dlp`.

```bash
# зависимости
uv sync

# системные утилиты
brew install ffmpeg
brew install yt-dlp      # только если планируешь скачивать по URL

# LLM для перевода
ollama pull llama3.1:8b
ollama serve
```

Первый запуск дополнительно скачает Silero-модель (~60 MB) в кеш `torch.hub`.

## Пайплайн

```
video.mp4 / URL
    │
    ▼
[1] transcribe.py   faster-whisper      текст + тайминги (Segment.original)
    │
    ▼
    group.py        слияние по gap      короткие сегменты склеиваются
    │                                   (max_duration-cap)
    ▼
[2] translate.py    Ollama /api/chat    перевод на RU с N=3 history
    │                                   (Segment.translated)
    ▼
[3] tts.py          Silero (v4_ru)      WAV на сегмент
    │                                   (Segment.audio_path/audio_duration)
    ▼
[4] merge.py        ffmpeg-python       atempo-стрейч + atrim-cap,
                                        amix поверх видео
    ▼
video_dubbed.mp4
```

Центральный объект — `Segment` (`segment.py`): `start`, `end`, `original`,
`translated`, `audio_path`, `audio_duration`.

## Синхронизация дубляжа

Русский перевод обычно на 20–50% длиннее оригинала, поэтому:

1. **`translate.py`** — в system-prompt подаётся length hint (`Keep the
   translation close to N characters`), чтобы LLM сам не раздувал длину.
2. **`tts.py`** — Silero синтезирует WAV, реальная длительность пишется в
   `Segment.audio_duration`.
3. **`merge.py`** — если `audio_duration > seg.duration`:
   - `atempo` с ratio, клэмп `ATEMPO_MAX = 1.25` (сохраняет pitch,
     ускоряет речь);
   - `atrim(duration=seg.duration)` как safety cap — без него хвост
     переливается в следующее окно и микшируется `amix` как «второй голос».
4. Если `audio_duration ≤ seg.duration` — фильтры не применяются,
   остаток окна остаётся тишиной.

`merge.py` печатает per-segment диагностику (`atempo=…, truncated …s`)
и итоговую строку сколько сегментов стрейчилось.

## Конфигурация

Все параметры в `config.yaml`:

```yaml
transcription:
  model: "base"          # tiny / base / small / medium / large
  device: "cpu"          # cpu | cuda | mps
  language: "auto"       # auto = определить автоматически, или "en", "ru" и т.д.

grouping:
  gap_threshold: 0.3     # сек — сегменты с gap меньше этого склеиваются
  max_duration: 12.0     # сек — верхний предел длительности склейки

translation:
  model: "llama3.1:8b"
  ollama_url: "http://localhost:11434"

tts:
  model: "v4_ru"         # Silero RU-бандл
  language: "ru"
  speaker: "eugene"      # aidar | eugene | baya | kseniya | xenia
  sample_rate: 48000

output:
  suffix: "_dubbed"
```

**Смена голоса:** поменять `speaker` в `config.yaml`. Клонирование голоса
Silero не поддерживает — если нужно, смотреть в сторону F5-TTS / XTTS.

## Стек

| Компонент | Инструмент | Назначение |
|---|---|---|
| Транскрипция | faster-whisper | Whisper, CPU, `int8` |
| Группировка | `group.py` | Склейка коротких Whisper-сегментов по `gap_threshold`, cap по `max_duration` |
| Перевод | Ollama (`/api/chat`, `llama3.1:8b`) | Sliding-window history N=3, `temperature=0`, length hint |
| Синтез речи | Silero TTS (`v4_ru`) | RU, подгружается через `torch.hub` из `snakers4/silero-models` |
| Сборка | ffmpeg / ffmpeg-python | Извлечение аудио, atempo-стрейч, amix |
| Загрузка URL | yt-dlp | Опционально — если вход является http(s)-ссылкой |

## Тесты

```bash
uv run pytest
```

Юнит-тесты покрывают `translate` (включая `_clean`, history, fallback),
`group`, `merge`, `tts`, `transcribe`, `dub`, `segment`.
