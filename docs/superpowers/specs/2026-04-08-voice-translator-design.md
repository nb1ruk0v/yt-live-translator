# Voice Translator Design — 2026-04-08

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
