# vt-claude — Video Translation & Dubbing

Пайплайн автоматического дубляжа видео: транскрипция → перевод → синтез речи → сборка.

## Быстрый старт

```bash
uv run dub.py data/test_video.mp4
```

Результат сохраняется рядом с исходником: `data/test_video_dubbed.mp4`.

## Установка

**Требования:** Python 3.11, [uv](https://github.com/astral-sh/uv), ffmpeg, [Ollama](https://ollama.ai)

```bash
# Установить зависимости
uv sync

# Убедиться что ffmpeg установлен
brew install ffmpeg

# Загрузить и запустить LLM
ollama pull llama3.1:8b
ollama serve
```

## Пайплайн

```
video.mp4
    │
    ▼
[1] transcribe.py   faster-whisper      извлекает текст + тайминги
    │
    ▼
[2] translate.py    Ollama LLM          переводит каждый сегмент на RU
    │
    ▼
[3] tts.py          Coqui XTTS v2       синтезирует WAV для каждого сегмента
    │
    ▼
[4] merge.py        ffmpeg-python       накладывает аудио на видео с таймингами
```

Центральный объект — `Segment` (`segment.py`): `start`, `end`, `original`, `translated`, `audio_path`.

## Конфигурация

Все параметры в `config.yaml`:

```yaml
transcription:
  model: "base"        # tiny / base / small / medium / large
  device: "cpu"        # cpu | cuda | mps
  language: "auto"     # auto = определить автоматически, или "en", "ru" и т.д.

translation:
  model: "llama3.1:8b"
  ollama_url: "http://localhost:11434"

tts:
  model: "tts_models/multilingual/multi-dataset/xtts_v2"
  language: "ru"
  speaker: "Claribel Dervla"   # встроенный голос
  speaker_wav: null             # путь к WAV для клонирования голоса (5–30 сек)

output:
  suffix: "_dubbed"
```

**Клонирование голоса:** укажи путь к WAV (5–30 сек, чистая речь) в `speaker_wav` — поле `speaker` при этом игнорируется.

## Стек

| Компонент | Инструмент | Назначение |
|---|---|---|
| Транскрипция | faster-whisper | Whisper, CPU, `int8` |
| Перевод | Ollama (`llama3.1:8b`) | Локальный LLM |
| Синтез речи | Coqui TTS (`xtts_v2`) | Многоязычная TTS-модель |
| Сборка | ffmpeg / ffmpeg-python | Наложение аудио на видео |

## Известные ограничения

- **transformers** зафиксирован на `<4.41` — в 4.41+ удалён `BeamSearchScorer`, который требует XTTS v2.
- **torch.load** в `.venv/.../TTS/utils/io.py` патчится вручную (`weights_only=False`) — PyTorch 2.6 изменил дефолт на `True`. При `uv sync` патч может быть перезаписан и его нужно применить заново.
