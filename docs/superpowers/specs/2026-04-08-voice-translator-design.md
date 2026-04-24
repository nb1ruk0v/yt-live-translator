# Voice Translator Design — 2026-04-08

> **Historical MVP spec.** Фиксирует исходное намерение на 2026-04-08.
> Фактический стек с тех пор эволюционировал — ниже отражено то, что было задумано, а не то, что работает сейчас. Актуальное состояние см. в `README.md` и `CLAUDE.md`.
>
> Ключевые отклонения от этого документа:
> - **TTS:** Coqui XTTS v2 → Silero (`v4_ru`). XTTS конфликтовал с `transformers>=4.41` и дефолтом `weights_only=True` в PyTorch 2.6; Silero стабильнее, без клонирования голоса.
> - **LLM:** `llama3.2:3b` → `llama3.1:8b`; `/api/generate` → `/api/chat` с N=3 history, `temperature=0` (см. `2026-04-18-context-aware-translation-design.md`).
> - **Sync:** `adelay` + `atrim` → length hint в system-prompt + `atempo` (cap 1.25) + `atrim` как safety cap.
> - **Группировка:** добавлен шаг `group.py` между transcribe и translate — склеивает короткие Whisper-сегменты по `gap_threshold` с cap по `max_duration`.

## Context
MVP-инструмент для дубляжа видео на русский язык. Всё локально, open source.
Будущее расширение — браузерный плагин для YouTube.

## Architecture
Линейный пайплайн: transcribe → translate → tts → merge.
Каждый шаг — отдельный модуль с единым форматом Segment.

## Stack
- Транскрипция: faster-whisper (base на CPU, large-v3 на GPU)
- Перевод: Ollama HTTP + llama3.2:3b
- TTS: Coqui XTTS-v2 (поддержка русского, voice cloning)
- Merge: ffmpeg-python

## Config
Все параметры моделей в config.yaml для быстрой смены.

## Sync Strategy
TTS-клип размещается по start-таймкоду через adelay.
Если длиннее слота — обрезается через atrim.
