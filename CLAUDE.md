# vt-claude — Video Translation & Dubbing

Пайплайн автоматического дубляжа видео: транскрипция → перевод → синтез речи → сборка.

## Запуск

```bash
uv run src/dub.py <video_file_or_url>
# локальный файл:
uv run src/dub.py data/test_video.mp4
# URL (через yt-dlp, сохраняется в data/):
uv run src/dub.py "https://www.youtube.com/watch?v=..."
```

Результат сохраняется рядом с исходником: `test_video_dubbed.mp4`.

## Архитектура

```
video.mp4 / URL
    │
    ▼
[1] src/transcribe.py   faster-whisper      извлекает текст + тайминги (Segment.original)
    │
    ▼
    src/group.py        склейка коротких сегментов по gap_threshold (с max_duration cap)
    │
    ▼
[2] src/translate.py    Ollama /api/chat    перевод на RU с N=3 history + length hint (Segment.translated)
    │
    ▼
[3] src/tts.py          Silero TTS (v4_ru)  синтезирует WAV для каждого сегмента (Segment.audio_path/audio_duration)
    │
    ▼
[4] src/merge.py        ffmpeg-python       atempo-стрейч + atrim-cap, amix поверх видео
```

Центральный объект — `Segment` (`src/segment.py`): `start`, `end`, `original`, `translated`, `audio_path`, `audio_duration`.

URL-вход детектируется `is_url` в `src/dub.py` и качается через `yt-dlp` (требуется в PATH).

## Зависимости и инфраструктура

| Что | Зачем |
|---|---|
| **faster-whisper** | Транскрипция речи (Whisper, CPU, `int8`) |
| **Ollama** (`llama3.1:8b`) | Локальный LLM для перевода, должен быть запущен (`ollama serve`) |
| **Silero TTS** (`v4_ru`) | Синтез речи на RU, подгружается через `torch.hub` из `snakers4/silero-models` |
| **ffmpeg** | Извлечение аудио и сборка финального видео, должен быть в PATH |
| **ffmpeg-python** | Python-обёртка над ffmpeg для `src/merge.py` |
| **yt-dlp** | Опционально — скачивание видео, если вход является http(s)-URL |

## Конфигурация (`config.yaml`)

```yaml
transcription:
  model: "base"        # размер модели Whisper: tiny/base/small/medium/large
  device: "cpu"        # cpu | cuda | mps
  language: "auto"     # auto = определить автоматически, или "en", "ru" и т.д.

grouping:
  gap_threshold: 0.3   # сек — сегменты с gap меньше этого склеиваются
  max_duration: 12.0   # сек — верхний предел длительности склейки

translation:
  model: "llama3.1:8b"
  ollama_url: "http://localhost:11434"

tts:
  model: "v4_ru"       # Silero RU-бандл
  language: "ru"
  speaker: "eugene"    # aidar | eugene | baya | kseniya | xenia
  sample_rate: 48000

output:
  suffix: "_dubbed"
```

**Смена голоса:** поменять `speaker` в `config.yaml`. Клонирование голоса Silero не поддерживает (если нужно — рассматривать F5-TTS / XTTS).

## Синхронизация дубляжа

Рус-перевод обычно на 20–50% длиннее оригинала, поэтому:

1. **`src/translate.py`** — в system-prompt подаётся length hint (`Keep the translation close to N characters ±20%`), чтобы LLM сам не раздувал длину.
2. **`src/tts.py`** — Silero синтезирует WAV, в `Segment.audio_duration` кладётся реальная длительность.
3. **`src/merge.py`** — если `audio_duration > seg.duration`:
   - `atempo` с ratio, клэмп `ATEMPO_MAX = 1.25` (сохраняет pitch, ускоряет речь);
   - `atrim(duration=seg.duration)` как safety cap, чтобы хвост не переливался в следующий сегмент (иначе `amix` микширует его как «второй голос»);
   - печатает per-segment диагностику + итоговую строку сколько сегментов стрейчилось.
4. Если `audio_duration ≤ seg.duration` — фильтры не применяются, остаток окна — тишина.

## Контекст перевода

`src/translate.py` обращается к Ollama через `/api/chat` с sliding-window history N=3 (локальная переменная функции, между запусками не сохраняется) и `temperature=0`. Постобработка ответа (`_clean`): trim пробелов и кавычек (`"`, `'`, `«`, `»`), при многострочном ответе — первая строка с кириллицей. Пустой оригинал → `translated = ""` без вызова. Невалидный ответ LLM (нет кириллицы) → фолбэк `translated = original` + предупреждение в stderr (пайплайн не роняется).

## Установка

```bash
uv sync
# убедиться что ffmpeg установлен:
brew install ffmpeg
# опционально — если планируешь скармливать URL:
brew install yt-dlp
# запустить Ollama с нужной моделью:
ollama pull llama3.1:8b
ollama serve
```

Первый запуск скачает Silero-модель (~60 MB) в кеш `torch.hub`.

## Тесты

```bash
uv run pytest
```

Покрытие: `translate` (`_clean`, history, fallback), `group`, `merge`, `tts`, `transcribe`, `dub`, `segment`.
