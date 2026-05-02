# aya-expanse:8b vs gemma4:e4b — A/B эксперимент

Дата: 2026-05-03
Backlog: пункт #28 из `docs/dubbing-improvements.md` (Фаза 1).

## Цель

Проверить гипотезу: специализированный мультиязычный `aya-expanse:8b` даёт перевод EN→RU лучше текущего `gemma4:e4b` на реальном материале (3 видео в `data/`).

Решение бинарное:
- если aya побеждает по тексту **и** звук на слух не хуже → swap `config.yaml` отдельным коммитом;
- если aya не лучше или хуже → фиксируем negative result в `experiments/results/` и закрываем пункт #28.

## Критерии оценки

**Текст (Claude review).** На side-by-side файле сравнить пары gemma/aya по четырём осям:
1. **Адекватность** — передан ли смысл оригинала.
2. **Стилистика** — естественность разговорной русской речи, отсутствие кальки.
3. **Грамматика** — согласования, падежи, окончания.
4. **Точность** — имена собственные, термины, числа.

Per-segment не оцениваем — по итогам читаем `.md` целиком и пишем агрегированный вердикт по каждой оси.

**Звук (user review).** Прослушать пары `_dubbed_gemma.mp4` / `_dubbed_aya.mp4` на тех же видео.

## Архитектура

```
experiments/aya_vs_gemma/
  run.py                                 — оркестратор
  <videoname>_translations.md            — side-by-side EN/gemma/aya per segment

data/
  <videoname>_dubbed_gemma.mp4
  <videoname>_dubbed_aya.mp4

experiments/results/
  2026-05-03-aya-vs-gemma.md             — финальный report (review + verdict)
```

## Алгоритм `run.py`

1. Загрузить `config.yaml`. Проверить prerequisites (как в `dub.py`) + наличие обеих моделей в Ollama (`/api/tags`). Если `aya-expanse:8b` отсутствует — abort с инструкцией `ollama pull aya-expanse:8b`.
2. Для каждого видео в `VIDEOS = [...]` (3 файла из `data/`):
   - `transcribe(video, cfg["transcription"])` → `group_segments(...)` → `base` (один раз — самая дорогая стадия).
   - Для каждой модели в `["gemma4:e4b", "aya-expanse:8b"]`:
     - `segs = deepcopy(base)` (важно: `Segment` мутируется в каждой стадии).
     - `translate(segs, {**cfg["translation"], "model": M})`.
     - `synthesize(segs, cfg["tts"])`.
     - `merge(video, segs, suffix=f"_dubbed_{tag}")` где `tag = "gemma"` / `"aya"`.
     - Сохранить `segs` в памяти для side-by-side дампа.
   - После обоих прогонов — записать `experiments/aya_vs_gemma/<videoname>_translations.md`.
3. В конце напечатать сводку: «6 dubbed mp4 + 3 translations.md ready for review».

## Формат side-by-side `.md`

Читаемый блочный формат, не таблица (длинные строки в таблице нечитаемы):

```markdown
# <videoname>

## [00:01:23.45 → 00:01:27.10] dur=3.65s

**EN:** Today we're going to walk through prompting best practices.
**gemma:** Сегодня мы пройдемся по лучшим практикам промптинга.
**aya:** Разберём лучшие практики промптинга.

## [00:01:27.10 → 00:01:32.40] dur=5.30s
...
```

Тайминги форматируются как `MM:SS.ms` (или `HH:MM:SS.ms` если видео > 1 часа).

## Не-цели (out of scope)

- Промпт-инжиниринг под aya (system prompt оставляем тот же — честное сравнение моделей, не промптов).
- Изменение temperature/seed (оставляем `temperature=0`).
- Свап TTS-голоса (Silero `kseniya`, как в production).
- Изменение `transcribe` / `group` — общий source-of-truth для обеих моделей.
- Любые правки в production-коде (`src/translate.py`, `src/dub.py`, `config.yaml`) до вердикта.

## Тонкости и риски

- **`Segment` мутируется** между стадиями (`translated`, `audio_path`, `audio_duration`). Между прогонами моделей обязателен `copy.deepcopy`. Альтернатива (выделить immutable structure) — out of scope для one-off эксперимента.
- **`aya-expanse:8b` ~5 GB** — pull до запуска (`ollama pull aya-expanse:8b`).
- **CPU-стоимость:** transcribe×3 (~15 мин/видео на turbo+CPU) + translate×6 (минуты) + TTS×6 (медленно) + merge×6. Итого порядка нескольких часов. Запускаем full-pipeline в один присест (вариант A в обсуждении).
- **`merge` пишет рядом с исходным видео** — outputs идут в `data/`, не в `experiments/`. Это OK; `experiments/aya_vs_gemma/` хранит только translations.md. Ради чистоты не рефакторим `merge`.
- **Side-by-side .md создаётся ПОСЛЕ обоих переводов**, не инкрементально, чтобы избежать частичных файлов при падении.
- **Тесты:** оркестратор — one-off скрипт в `experiments/`, не покрываем юнит-тестами (как `experiments/transcribe_compare/` и `experiments/trim_silence/`).

## DoD

1. `experiments/aya_vs_gemma/run.py` отработал без ошибок на всех 3 видео.
2. В `data/` появились 6 файлов `<videoname>_dubbed_{gemma,aya}.mp4`.
3. В `experiments/aya_vs_gemma/` появились 3 файла `<videoname>_translations.md`.
4. В `experiments/results/2026-05-03-aya-vs-gemma.md` записан Claude-review (4 оси × 3 видео) + user-review звука + финальный вердикт.
5. Если вердикт «aya wins» — отдельный коммит со swap'ом `translation.model` в `config.yaml` + обновление `CLAUDE.md` (упоминание модели).
6. Если вердикт «no win» — закрытие пункта #28 в `docs/dubbing-improvements.md` с пометкой «проверено и отклонено» (паттерн `#11`).
