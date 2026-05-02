# aya-vs-gemma A/B — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Сравнить переводы EN→RU моделями `gemma4:e4b` и `aya-expanse:8b` на 3 локальных видео, получить 6 dubbed mp4 + 3 side-by-side `.md` для review, вынести вердикт о swap'е production-модели.

**Архитектура:** Один оркестратор `experiments/aya_vs_gemma/run.py`. Для каждого видео `transcribe + group` запускается **один раз**, дальше segments копируются (`deepcopy`) и прогоняются через `translate → synthesize → merge` для каждой модели независимо. Production-код (`src/*`, `config.yaml`) не изменяется до вердикта.

**Tech Stack:** Python 3.11, существующие модули `src/{transcribe,group,translate,tts,merge}.py`, Ollama API, `argparse` для smoke-флага.

**Spec:** `docs/superpowers/specs/2026-05-03-aya-vs-gemma-design.md`

---

## File Structure

- **Create:** `experiments/aya_vs_gemma/run.py` — оркестратор A/B (≈150 строк).
- **Create:** `experiments/aya_vs_gemma/<videoname>_translations.md` — артефакты (генерируются скриптом, не коммитим? см. ниже).
- **Create:** `experiments/results/2026-05-03-aya-vs-gemma.md` — финальный report (Claude text-review + user audio-review + вердикт).
- **Modify (только при вердикте «aya wins»):** `config.yaml` — поле `translation.model`.
- **Modify (только при вердикте «no win»):** `docs/dubbing-improvements.md` — пункт #28 в Фазе 1 → пометка «проверено и отклонено».

Артефакты `.md` с переводами — коммитим (как `experiments/transcribe_compare/results/`). Артефакты `.mp4` (×6) — НЕ коммитим (бинари; 6 файлов, > 100 MB суммарно). Добавим в `.gitignore` префикс `data/*_dubbed_*.mp4` если ещё нет.

---

### Task 1: Bootstrap `run.py` skeleton

**Files:**
- Create: `experiments/aya_vs_gemma/run.py`

- [ ] **Step 1: Создать файл со скелетом**

```python
"""A/B-сравнение моделей перевода gemma4:e4b vs aya-expanse:8b.

Spec: docs/superpowers/specs/2026-05-03-aya-vs-gemma-design.md
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
HERE = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "src"))

VIDEOS = [
    "From Vibe Coding to Agentic Engineering.mp4",
    "Mastering Claude Code in 30 minutes.mp4",
    "Prompting for Agents.mp4",
]

MODEL_TAGS = {
    "gemma4:e4b": "gemma",
    "aya-expanse:8b": "aya",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--skip-audio",
        action="store_true",
        help="Skip TTS+merge, only produce translations.md (fast smoke mode).",
    )
    p.add_argument(
        "videos",
        nargs="*",
        help="Optional subset of video filenames (default: all 3 in VIDEOS).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    videos = args.videos or VIDEOS
    print(f"[ab] videos: {videos}")
    print(f"[ab] skip_audio: {args.skip_audio}")
    print(f"[ab] models: {list(MODEL_TAGS)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke**

Run: `uv run experiments/aya_vs_gemma/run.py --help`
Expected: argparse usage напечатан, exit 0.

Run: `uv run experiments/aya_vs_gemma/run.py --skip-audio`
Expected: 3 print-строки `[ab] videos:`, `[ab] skip_audio: True`, `[ab] models:`.

- [ ] **Step 3: Commit**

```bash
git add experiments/aya_vs_gemma/run.py
git commit -m "experiment(aya-vs-gemma): bootstrap run.py skeleton"
```

---

### Task 2: Config loading + Ollama models check

**Files:**
- Modify: `experiments/aya_vs_gemma/run.py`

- [ ] **Step 1: Добавить imports и helpers**

Заменить блок `import argparse...` и добавить функции после констант. Целевое состояние верхней части файла:

```python
import argparse
import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
HERE = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT / "src"))

VIDEOS = [...]  # без изменений
MODEL_TAGS = {...}  # без изменений


def load_config() -> dict:
    with open(ROOT / "config.yaml") as f:
        return yaml.safe_load(f)


def check_ollama_models(ollama_url: str, required: list[str]) -> None:
    r = requests.get(f"{ollama_url}/api/tags", timeout=5)
    r.raise_for_status()
    available = {m["name"] for m in r.json().get("models", [])}
    missing = [m for m in required if m not in available]
    if missing:
        raise RuntimeError(
            f"Missing Ollama models: {missing}. Pull with: "
            + " && ".join(f"ollama pull {m}" for m in missing)
        )
```

- [ ] **Step 2: Вызвать check в main()**

Заменить тело `main()`:

```python
def main() -> None:
    args = parse_args()
    videos = args.videos or VIDEOS
    cfg = load_config()
    check_ollama_models(cfg["translation"]["ollama_url"], list(MODEL_TAGS))
    print(f"[ab] videos: {videos}")
    print(f"[ab] skip_audio: {args.skip_audio}")
    print(f"[ab] models OK: {list(MODEL_TAGS)}")
```

- [ ] **Step 3: Smoke (оба варианта — модель есть и нет)**

Run: `uv run experiments/aya_vs_gemma/run.py --skip-audio`
Expected (если `aya-expanse:8b` уже pulled): печатает `[ab] models OK: [...]`.
Expected (если ещё качается): `RuntimeError: Missing Ollama models: ['aya-expanse:8b']. Pull with: ollama pull aya-expanse:8b` — это валидная ошибка, ждём окончания pull.

- [ ] **Step 4: Commit**

```bash
git add experiments/aya_vs_gemma/run.py
git commit -m "experiment(aya-vs-gemma): config + Ollama models check"
```

---

### Task 3: Helpers `format_time` и `format_translations_md`

**Files:**
- Modify: `experiments/aya_vs_gemma/run.py`

- [ ] **Step 1: Добавить helpers (после `check_ollama_models`)**

```python
def format_time(seconds: float) -> str:
    """`MM:SS.ms` для коротких видео, `HH:MM:SS.ms` для длинных."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = seconds % 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{sec:06.3f}"
    return f"{minutes:02d}:{sec:06.3f}"


def format_translations_md(
    video_name: str,
    gemma_segs: list,  # list[Segment]
    aya_segs: list,    # list[Segment]
) -> str:
    assert len(gemma_segs) == len(aya_segs), "segment count mismatch"
    lines = [f"# {video_name}", ""]
    for g, a in zip(gemma_segs, aya_segs):
        assert g.start == a.start and g.end == a.end, "timing drift between models"
        lines.append(
            f"## [{format_time(g.start)} → {format_time(g.end)}] dur={g.duration:.2f}s"
        )
        lines.append("")
        lines.append(f"**EN:** {g.original}")
        lines.append(f"**gemma:** {g.translated}")
        lines.append(f"**aya:** {a.translated}")
        lines.append("")
    return "\n".join(lines)
```

- [ ] **Step 2: Inline self-check в main()**

Добавить **перед** `print(f"[ab] videos:")`:

```python
    # self-check helpers
    assert format_time(75.5) == "01:15.500", f"format_time bug: {format_time(75.5)}"
    assert format_time(3725.5) == "01:02:05.500", f"format_time bug: {format_time(3725.5)}"
```

- [ ] **Step 3: Smoke**

Run: `uv run experiments/aya_vs_gemma/run.py --skip-audio`
Expected: ассерты прошли, печатает `[ab] models OK`.

- [ ] **Step 4: Commit**

```bash
git add experiments/aya_vs_gemma/run.py
git commit -m "experiment(aya-vs-gemma): time + translations-md formatters"
```

---

### Task 4: Translate-only main loop (без TTS/merge)

**Files:**
- Modify: `experiments/aya_vs_gemma/run.py`

- [ ] **Step 1: Добавить imports из src/**

В начало файла, после `import yaml`:

```python
from copy import deepcopy

# from src/
from group import group_segments
from transcribe import transcribe
from translate import translate
```

- [ ] **Step 2: Добавить функцию `process_video()` после хелперов**

```python
def process_video(video_name: str, cfg: dict, skip_audio: bool) -> None:
    video_path = DATA / video_name
    if not video_path.exists():
        raise FileNotFoundError(video_path)

    print(f"\n[ab] === {video_name} ===")

    print("[ab] [1/3] transcribe + group (once)")
    base = transcribe(str(video_path), cfg["transcription"])
    grouping = cfg.get("grouping", {})
    base = group_segments(
        base,
        gap_threshold=grouping.get("gap_threshold", 0.3),
        max_duration=grouping.get("max_duration", 12.0),
    )
    print(f"[ab]      base segments: {len(base)}")

    per_model: dict[str, list] = {}
    for model_name, tag in MODEL_TAGS.items():
        print(f"[ab] [2/3] translate ({model_name})")
        segs = deepcopy(base)
        translate(segs, {**cfg["translation"], "model": model_name})
        per_model[tag] = segs

    md_path = HERE / f"{Path(video_name).stem}_translations.md"
    md_path.write_text(format_translations_md(video_name, per_model["gemma"], per_model["aya"]))
    print(f"[ab]      wrote {md_path.relative_to(ROOT)}")

    if skip_audio:
        print("[ab] [3/3] skipped (--skip-audio)")
        return

    # TTS+merge будет добавлен в Task 6
    raise NotImplementedError("audio path will be added in Task 6")
```

- [ ] **Step 2.1: Подключить `process_video` в `main()`**

Заменить тело `main()` (после ассертов и check_ollama_models):

```python
def main() -> None:
    args = parse_args()
    videos = args.videos or VIDEOS
    cfg = load_config()
    check_ollama_models(cfg["translation"]["ollama_url"], list(MODEL_TAGS))

    assert format_time(75.5) == "01:15.500", f"format_time bug: {format_time(75.5)}"
    assert format_time(3725.5) == "01:02:05.500", f"format_time bug: {format_time(3725.5)}"

    print(f"[ab] videos: {videos}")
    print(f"[ab] skip_audio: {args.skip_audio}")

    for v in videos:
        process_video(v, cfg, skip_audio=args.skip_audio)

    print(f"\n[ab] done. translations: {len(videos)}, audio: {0 if args.skip_audio else len(videos) * 2}")
```

- [ ] **Step 3: Commit (smoke в Task 5)**

```bash
git add experiments/aya_vs_gemma/run.py
git commit -m "experiment(aya-vs-gemma): translate-only main loop"
```

---

### Task 5: Smoke — translate-only на одном видео

**Files:** read-only (артефакт `.md` будет создан, но не коммитим до полного прогона).

- [ ] **Step 1: Запустить translate-only на shortest video**

Run:
```bash
uv run experiments/aya_vs_gemma/run.py --skip-audio "Mastering Claude Code in 30 minutes.mp4"
```

Expected:
- Печатает `[ab] === Mastering Claude Code in 30 minutes.mp4 ===`
- Печатает `[ab] [1/3] transcribe + group (once)` и `base segments: ~250`
- Дважды печатает `[ab] [2/3] translate (...)` (gemma + aya)
- Печатает `wrote experiments/aya_vs_gemma/Mastering Claude Code in 30 minutes_translations.md`
- Печатает `[ab] [3/3] skipped (--skip-audio)`
- Печатает финальную сводку `done. translations: 1, audio: 0`
- Exit 0

Время: ~10–20 мин (transcribe ~10 мин на CPU + translate ×2 быстро).

- [ ] **Step 2: Проверить артефакт глазами**

Read: `experiments/aya_vs_gemma/Mastering Claude Code in 30 minutes_translations.md`
Expected:
- Заголовок `# Mastering Claude Code in 30 minutes.mp4`
- Блоки `## [MM:SS.ms → MM:SS.ms] dur=...s` с `**EN:**`, `**gemma:**`, `**aya:**`
- В обеих переводах кириллица, осмысленный текст
- Тайминги монотонно растут

Если что-то не так (нет кириллицы у aya, кривые тайминги, kosaks нечитаемы) — стоп, чинить.

- [ ] **Step 3: Не коммитим .md** — будет коммит после full run в Task 8.

---

### Task 6: TTS + merge для обеих моделей

**Files:**
- Modify: `experiments/aya_vs_gemma/run.py`

- [ ] **Step 1: Добавить imports**

В блок импортов из `src/`:

```python
from merge import merge
from tts import synthesize
```

- [ ] **Step 2: Заменить `NotImplementedError` блок на TTS+merge**

В `process_video()` заменить блок:

```python
    if skip_audio:
        print("[ab] [3/3] skipped (--skip-audio)")
        return

    raise NotImplementedError("audio path will be added in Task 6")
```

на:

```python
    if skip_audio:
        print("[ab] [3/3] skipped (--skip-audio)")
        return

    for tag, segs in per_model.items():
        print(f"[ab] [3/3] synthesize+merge ({tag})")
        synthesize(segs, cfg["tts"])
        out = merge(str(video_path), segs, suffix=f"_dubbed_{tag}")
        print(f"[ab]      wrote {out}")
```

- [ ] **Step 3: Commit (smoke в Task 7)**

```bash
git add experiments/aya_vs_gemma/run.py
git commit -m "experiment(aya-vs-gemma): TTS + merge for both models"
```

---

### Task 7: Smoke — full pipeline на одном видео

- [ ] **Step 1: Запустить полный прогон на shortest video**

Run:
```bash
uv run experiments/aya_vs_gemma/run.py "Mastering Claude Code in 30 minutes.mp4"
```

Expected:
- Все шаги Task 5 +
- Дважды `[ab] [3/3] synthesize+merge (...)` (gemma + aya)
- Печатает `wrote .../Mastering Claude Code in 30 minutes_dubbed_gemma.mp4`
- Печатает `wrote .../Mastering Claude Code in 30 minutes_dubbed_aya.mp4`
- Финальная сводка `done. translations: 1, audio: 2`
- Exit 0

Время: ~40–60 мин (TTS ×2 — самое медленное).

- [ ] **Step 2: Проверить файлы**

Run: `ls -la "data/Mastering Claude Code in 30 minutes_dubbed_"*.mp4`
Expected: 2 файла, оба > 1 MB.

Запустить хотя бы первые 30 секунд каждого в плеере (визуально и на слух) — что речь идёт, не пустота.

Если что-то не так (один из файлов не создался, тишина, треск) — стоп, чинить.

---

### Task 8: Full run на всех 3 видео + коммит артефактов `.md`

- [ ] **Step 1: Запустить весь набор**

Run:
```bash
uv run experiments/aya_vs_gemma/run.py
```

Expected:
- Прогон 3 видео × full pipeline
- 3 `_translations.md` в `experiments/aya_vs_gemma/`
- 6 `_dubbed_{gemma,aya}.mp4` в `data/`
- Exit 0

Время: ~3–5 часов (CPU-bound на TTS).

Если упадёт посередине — определить какое видео, запустить остаток `uv run ... "Video 2.mp4" "Video 3.mp4"`.

- [ ] **Step 2: Защититься от случайного коммита mp4**

Добавить в `.gitignore` (если нет):

```
data/*_dubbed_*.mp4
```

- [ ] **Step 3: Коммит артефактов**

```bash
git add .gitignore experiments/aya_vs_gemma/*_translations.md
git commit -m "experiment(aya-vs-gemma): translation artifacts for 3 videos"
```

---

### Task 9: Claude text-review

**Files:**
- Create: `experiments/results/2026-05-03-aya-vs-gemma.md`

- [ ] **Step 1: Прочитать все 3 `*_translations.md`**

Read каждый файл целиком, выделить:
- Случаи где gemma явно хуже aya (или наоборот) — с цитатой и таймингом.
- Систематические паттерны (например, aya дословнее, gemma вольнее; aya лучше с терминами; etc.).
- Грамматические/стилистические проколы.

- [ ] **Step 2: Записать report**

Шаблон `experiments/results/2026-05-03-aya-vs-gemma.md`:

```markdown
# aya-expanse:8b vs gemma4:e4b — A/B результаты

Дата: 2026-05-03
Spec: docs/superpowers/specs/2026-05-03-aya-vs-gemma-design.md
Plan: docs/superpowers/plans/2026-05-03-aya-vs-gemma.md

## Setup

- 3 видео из `data/`: ...
- transcribe + group: один раз на видео (общий source)
- translate: gemma4:e4b и aya-expanse:8b, остальные параметры (system prompt, history N=3, temp=0) идентичны
- TTS: Silero v4_ru, голос kseniya

## Claude text-review

### Адекватность (передача смысла)
[агрегированно по 3 видео + 2-3 показательные цитаты с таймингами]

### Стилистика
[...]

### Грамматика
[...]

### Точность (имена, термины, числа)
[...]

### Сводный текстовый вердикт
gemma | aya | tie — почему

## User audio-review

(заполнит пользователь после прослушивания .mp4 пар)

## Финальный вердикт

(заполняется после обоих review)
- [ ] swap: `config.yaml` translation.model → aya-expanse:8b
- [ ] no win: пункт #28 закрыт как rejected в `docs/dubbing-improvements.md`
```

- [ ] **Step 3: Commit (без вердикта пока)**

```bash
git add experiments/results/2026-05-03-aya-vs-gemma.md
git commit -m "experiment(aya-vs-gemma): Claude text-review"
```

---

### Task 10: User audio-review + финальный вердикт

- [ ] **Step 1: User слушает 6 mp4**

Файлы в `data/`:
- `From Vibe Coding to Agentic Engineering_dubbed_{gemma,aya}.mp4`
- `Mastering Claude Code in 30 minutes_dubbed_{gemma,aya}.mp4`
- `Prompting for Agents_dubbed_{gemma,aya}.mp4`

Critical points: естественность интонации (TTS одинаковый — но длина перевода влияет на atempo), синхронность с видео, отсутствие явных ошибок произношения из-за длинных слов.

- [ ] **Step 2: User записывает заметки в раздел `## User audio-review`**

- [ ] **Step 3: Совместный финальный вердикт в `## Финальный вердикт`**

Заполнить один из двух чекбоксов.

- [ ] **Step 4: Commit вердикта**

```bash
git add experiments/results/2026-05-03-aya-vs-gemma.md
git commit -m "experiment(aya-vs-gemma): final verdict"
```

---

### Task 11a: (Conditional, если aya wins) Swap production model

**Files:**
- Modify: `config.yaml` — поле `translation.model`
- Modify: `CLAUDE.md` — упоминание модели в разделе «Зависимости и инфраструктура» и/или «Установка»

- [ ] **Step 1: Поменять `config.yaml`**

```diff
 translation:
-  model: "gemma4:e4b"
+  model: "aya-expanse:8b"
```

- [ ] **Step 2: Поменять упоминания в `CLAUDE.md`**

Заменить `gemma4:e4b` → `aya-expanse:8b` (и в строке `ollama pull gemma4:e4b` → `ollama pull aya-expanse:8b`).

- [ ] **Step 3: Прогнать тесты**

Run: `uv run pytest`
Expected: все зелёные (тесты в `test_translate.py` мокают HTTP, model name в них не критичен — должны пройти без изменений).

- [ ] **Step 4: Закрыть пункт #28 в backlog**

Modify: `docs/dubbing-improvements.md`, строка 812 (Фаза 1, пункт #28):

Заменить:
```
1. **#28 заменить gemma:e4b на aya-expanse:8b** (5 / 50). Один config-change + `ollama pull`. Самое дешёвое улучшение перевода в принципе. Делать первым, до любых правок в `translate.py` — иначе мы будем оптимизировать промпт под не лучшую модель.
```

на:
```
1. ~~**#28 заменить gemma:e4b на aya-expanse:8b** (5 / 50).~~ **Сделано** (2026-05-03): см. `experiments/results/2026-05-03-aya-vs-gemma.md`.
```

- [ ] **Step 5: Commit**

```bash
git add config.yaml CLAUDE.md docs/dubbing-improvements.md
git commit -m "feat(translate): swap to aya-expanse:8b (closes #28)"
```

---

### Task 11b: (Conditional, если no win) Пометить #28 rejected

**Files:**
- Modify: `docs/dubbing-improvements.md`

- [ ] **Step 1: Пометить #28 rejected (паттерн как у #11)**

Заменить строку 812:
```
1. ~~**#28 заменить gemma:e4b на aya-expanse:8b** (5 / 50).~~ **Проверено и отклонено** (2026-05-03): [краткое резюме почему]. См. `experiments/results/2026-05-03-aya-vs-gemma.md`.
```

- [ ] **Step 2: Commit**

```bash
git add docs/dubbing-improvements.md
git commit -m "docs(aya-vs-gemma): record negative result + close #28"
```

---

### Task 12: Merge ветки в main

- [ ] **Step 1: Sanity check**

Run: `git status` (clean), `uv run pytest` (зелёные).

- [ ] **Step 2: Merge или PR**

Зависит от практики юзера. Если PR — `gh pr create`; если direct merge — `git checkout main && git merge experiment/aya-vs-gemma --no-ff`.

(Этот шаг обсудить с юзером — не делать автоматически.)

---

## Self-Review (выполнено перед сохранением плана)

- **Spec coverage:** все 5 пунктов DoD из спеки покрыты тасками: (1) run.py отработал — Task 8; (2) 6 mp4 — Task 8; (3) 3 .md — Task 8; (4) report с verdict — Task 9+10; (5) swap или close — Task 11a/11b.
- **Placeholder scan:** нет TBD/«implement later». Все блоки с кодом — финальные.
- **Type consistency:** `Segment` (dataclass) — единственный тип, передаётся list[Segment] везде. `MODEL_TAGS` dict с консистентными ключами и значениями.
- **Зависимости между тасками:** Task 4 опирается на helpers из Task 3. Task 6 на process_video из Task 4. Task 7 — smoke для Task 6. Tasks 5 и 7 — gating smoke без commit. Tasks 11a/11b — взаимоисключающие.
