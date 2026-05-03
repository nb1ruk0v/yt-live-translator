# SRT Sidecar Subtitles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** После прогона `dub.py` записывать рядом с output mp4 два sidecar SRT-файла (`.en.srt` оригинал, `.ru.srt` перевод), чтобы плеер автоподхватывал их по совпадающему стему.

**Архитектура:** Один новый модуль `src/subtitles.py` (writer + helpers, ~30–40 строк), три строки wire-up в `src/dub.py` после `merge()`. Никаких изменений в `transcribe.py`, `translate.py`, `tts.py`, `merge.py`, `segment.py`, `config.yaml`. TDD: helpers и writer покрываются юнит-тестами в `tests/test_subtitles.py` до реализации.

**Tech Stack:** Python 3.11, stdlib (`textwrap`, `pathlib`), существующий `Segment` dataclass, pytest для тестов.

**Spec:** `docs/superpowers/specs/2026-05-03-srt-subtitles-design.md`

---

## File Structure

- **Create:** `src/subtitles.py` — `write_srt()` + `_format_timecode`, `_wrap`, `_escape`. Один модуль с одним публичным API, т.к. фича маленькая и связная.
- **Create:** `tests/test_subtitles.py` — юнит-тесты по таблице из spec. Группировка по helper'ам (`TestFormatTimecode`, `TestWrap`, `TestEscape`, `TestWriteSrt`) — как в `tests/test_translate.py`.
- **Modify:** `src/dub.py` — после `merge()` добавить запись двух sidecar файлов; счётчики шагов `[N/4]` → `[N/5]`. Импорт `from subtitles import write_srt`.
- **Modify:** `docs/dubbing-improvements.md` — пункт #14 → `Status (2026-05-03): Сделано` со ссылкой на отчёт; зачёркивание в Фазе 1.
- **Create:** `experiments/results/2026-05-03-srt-subtitles.md` — отчёт по DoD (cue counts, валидация, скриншот плеера, sanity таймингов).

Импорт в `tests/test_subtitles.py` идёт как `from subtitles import ...` (благодаря `pyproject.toml: pythonpath = ["src"]`).

---

### Task 1: Worktree и ветка

**Files:**
- Воркспейс: новый git worktree `../vt-claude-srt-subtitles` на ветке `feature/srt-subtitles` (от `main`).

- [ ] **Step 1: Создать worktree и ветку**

```bash
cd /Users/nbirukov/Courses/vt-claude
git worktree add ../vt-claude-srt-subtitles -b feature/srt-subtitles main
cd ../vt-claude-srt-subtitles
```

Expected: worktree создан, текущая ветка `feature/srt-subtitles`, рабочее дерево чистое.

- [ ] **Step 2: Verify**

Run: `git status && git branch --show-current && pwd`
Expected: `working tree clean`, `feature/srt-subtitles`, путь оканчивается на `vt-claude-srt-subtitles`.

Все последующие команды выполняются из `../vt-claude-srt-subtitles`.

---

### Task 2: `_format_timecode` — TDD

**Files:**
- Create: `src/subtitles.py`
- Create: `tests/test_subtitles.py`

- [ ] **Step 1: Создать тесты для `_format_timecode`**

Записать в `tests/test_subtitles.py`:

```python
from subtitles import _format_timecode


class TestFormatTimecode:
    def test_zero(self):
        assert _format_timecode(0.0) == "00:00:00,000"

    def test_subsecond_milliseconds(self):
        assert _format_timecode(1.234) == "00:00:01,234"

    def test_hours_minutes_seconds(self):
        # 1h 1m 1.5s
        assert _format_timecode(3661.5) == "01:01:01,500"

    def test_milliseconds_round_up_carries_to_seconds(self):
        # 0.9999 * 1000 = 999.9 → round → 1000ms → carry to 1.000s
        assert _format_timecode(0.9999) == "00:00:01,000"

    def test_milliseconds_round_down(self):
        assert _format_timecode(0.0004) == "00:00:00,000"
```

- [ ] **Step 2: Создать пустой `src/subtitles.py` и убедиться что тесты падают**

```python
# src/subtitles.py
"""Sidecar SRT subtitle writer.

Spec: docs/superpowers/specs/2026-05-03-srt-subtitles-design.md
"""
```

Run: `uv run pytest tests/test_subtitles.py -v`
Expected: 5 FAIL с `ImportError: cannot import name '_format_timecode'`.

- [ ] **Step 3: Реализовать `_format_timecode`**

Дописать в `src/subtitles.py`:

```python
def _format_timecode(seconds: float) -> str:
    """Format seconds as 'HH:MM:SS,mmm' (SRT timecode, comma decimal)."""
    total_ms = round(seconds * 1000)
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
```

- [ ] **Step 4: Run тестов**

Run: `uv run pytest tests/test_subtitles.py::TestFormatTimecode -v`
Expected: 5 PASS.

- [ ] **Step 5: Commit**

```bash
git add src/subtitles.py tests/test_subtitles.py
git commit -m "feat(subtitles): _format_timecode helper"
```

---

### Task 3: `_wrap` — TDD

**Files:**
- Modify: `src/subtitles.py`
- Modify: `tests/test_subtitles.py`

- [ ] **Step 1: Дописать тесты для `_wrap`**

Дополнить `tests/test_subtitles.py`:

```python
from subtitles import _format_timecode, _wrap


class TestWrap:
    def test_short_text_single_line(self):
        assert _wrap("Hello world") == "Hello world"

    def test_long_text_two_lines(self):
        # ~60 chars → must split into 2 lines, each ≤42
        text = "Today we are going to walk through prompting best practices today"
        result = _wrap(text)
        lines = result.split("\n")
        assert len(lines) == 2
        assert all(len(line) <= 42 for line in lines)

    def test_overflow_truncates_with_ellipsis(self):
        # Very long text → 2 lines, last ends with "…"
        text = "word " * 60  # 300 chars of "word word word..."
        result = _wrap(text)
        lines = result.split("\n")
        assert len(lines) == 2
        assert lines[1].endswith("…")
        assert all(len(line) <= 42 for line in lines)

    def test_exact_two_lines_no_ellipsis(self):
        # Fits exactly in 2 lines without truncation → no ellipsis
        text = "a" * 30 + " " + "b" * 30  # 61 chars, splits 30/30 by space
        result = _wrap(text)
        lines = result.split("\n")
        assert len(lines) == 2
        assert not lines[1].endswith("…")
```

- [ ] **Step 2: Run для убеждения что падает**

Run: `uv run pytest tests/test_subtitles.py::TestWrap -v`
Expected: 4 FAIL с `ImportError: cannot import name '_wrap'`.

- [ ] **Step 3: Реализовать `_wrap`**

Дописать в `src/subtitles.py` (вверху файла):

```python
import textwrap
```

И функцию:

```python
def _wrap(text: str, width: int = 42, max_lines: int = 2) -> str:
    """Wrap text into at most `max_lines` of `width` chars; truncate with '…' if overflow."""
    lines = textwrap.wrap(text, width=width)
    if len(lines) <= max_lines:
        return "\n".join(lines)
    kept = lines[:max_lines]
    # Trim last line to fit width including ellipsis
    last = kept[-1]
    if len(last) + 1 > width:
        last = last[: width - 1].rstrip()
    kept[-1] = last + "…"
    return "\n".join(kept)
```

- [ ] **Step 4: Run тестов**

Run: `uv run pytest tests/test_subtitles.py::TestWrap -v`
Expected: 4 PASS.

- [ ] **Step 5: Commit**

```bash
git add src/subtitles.py tests/test_subtitles.py
git commit -m "feat(subtitles): _wrap helper with overflow ellipsis"
```

---

### Task 4: `_escape` — TDD

**Files:**
- Modify: `src/subtitles.py`
- Modify: `tests/test_subtitles.py`

- [ ] **Step 1: Дописать тесты для `_escape`**

Дополнить `tests/test_subtitles.py`:

```python
from subtitles import _escape, _format_timecode, _wrap


class TestEscape:
    def test_strips_outer_whitespace(self):
        assert _escape("  hello  ") == "hello"

    def test_collapses_internal_newlines_to_space(self):
        assert _escape("line1\nline2") == "line1 line2"

    def test_collapses_carriage_returns(self):
        assert _escape("line1\r\nline2") == "line1 line2"

    def test_replaces_arrow_sequence(self):
        assert _escape("a-->b") == "a‐‐>b"

    def test_combined(self):
        assert _escape("  a-->b\nc  ") == "a‐‐>b c"
```

- [ ] **Step 2: Run для проверки падения**

Run: `uv run pytest tests/test_subtitles.py::TestEscape -v`
Expected: 5 FAIL с `ImportError: cannot import name '_escape'`.

- [ ] **Step 3: Реализовать `_escape`**

Дописать в `src/subtitles.py`:

```python
def _escape(text: str) -> str:
    """Strip whitespace, collapse internal newlines to space, neutralize '-->' sequence."""
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ")
    text = text.replace("-->", "‐‐>")  # en-dash chars, not hyphen-minus
    return text.strip()
```

- [ ] **Step 4: Run тестов**

Run: `uv run pytest tests/test_subtitles.py::TestEscape -v`
Expected: 5 PASS.

- [ ] **Step 5: Commit**

```bash
git add src/subtitles.py tests/test_subtitles.py
git commit -m "feat(subtitles): _escape helper for SRT-unsafe chars"
```

---

### Task 5: `write_srt` — happy path TDD

**Files:**
- Modify: `src/subtitles.py`
- Modify: `tests/test_subtitles.py`

- [ ] **Step 1: Дописать тесты для `write_srt`**

Дополнить `tests/test_subtitles.py`:

```python
from segment import Segment
from subtitles import _escape, _format_timecode, _wrap, write_srt


def _seg(start, end, original="", translated=""):
    return Segment(start=start, end=end, original=original, translated=translated)


class TestWriteSrt:
    def test_basic_two_segments_en(self, tmp_path):
        segs = [
            _seg(0.0, 1.5, original="Hello world."),
            _seg(2.0, 4.25, original="This is segment two."),
        ]
        path = tmp_path / "out.en.srt"
        n = write_srt(segs, str(path), lang="en")
        assert n == 2
        expected = (
            "1\n"
            "00:00:00,000 --> 00:00:01,500\n"
            "Hello world.\n"
            "\n"
            "2\n"
            "00:00:02,000 --> 00:00:04,250\n"
            "This is segment two.\n"
            "\n"
        )
        assert path.read_text(encoding="utf-8") == expected

    def test_basic_two_segments_ru(self, tmp_path):
        segs = [
            _seg(0.0, 1.0, original="Hi.", translated="Привет."),
            _seg(1.0, 2.0, original="Bye.", translated="Пока."),
        ]
        path = tmp_path / "out.ru.srt"
        n = write_srt(segs, str(path), lang="ru")
        assert n == 2
        content = path.read_text(encoding="utf-8")
        assert "Привет." in content
        assert "Пока." in content
        assert "Hi." not in content

    def test_returns_cue_count(self, tmp_path):
        segs = [_seg(0.0, 1.0, original="A.")]
        path = tmp_path / "out.en.srt"
        assert write_srt(segs, str(path), lang="en") == 1
```

- [ ] **Step 2: Run для проверки падения**

Run: `uv run pytest tests/test_subtitles.py::TestWriteSrt -v`
Expected: 3 FAIL с `ImportError: cannot import name 'write_srt'`.

- [ ] **Step 3: Реализовать `write_srt` (happy path, без edge cases)**

Дописать в `src/subtitles.py`:

```python
from typing import Literal

from segment import Segment


def write_srt(
    segments: list[Segment], path: str, lang: Literal["en", "ru"]
) -> int:
    """Write `segments` as SRT to `path`. Returns count of cues written.

    `lang="en"` uses seg.original; `lang="ru"` uses seg.translated.
    Existing files at `path` are overwritten.
    """
    count = 0
    with open(path, "w", encoding="utf-8") as f:
        for seg in segments:
            text = seg.original if lang == "en" else seg.translated
            text = _escape(text)
            text = _wrap(text)
            count += 1
            f.write(f"{count}\n")
            f.write(f"{_format_timecode(seg.start)} --> {_format_timecode(seg.end)}\n")
            f.write(f"{text}\n\n")
    return count
```

- [ ] **Step 4: Run тестов**

Run: `uv run pytest tests/test_subtitles.py::TestWriteSrt -v`
Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
git add src/subtitles.py tests/test_subtitles.py
git commit -m "feat(subtitles): write_srt happy path"
```

---

### Task 6: `write_srt` — edge cases

**Files:**
- Modify: `src/subtitles.py`
- Modify: `tests/test_subtitles.py`

- [ ] **Step 1: Дописать edge-case тесты**

Дополнить класс `TestWriteSrt` в `tests/test_subtitles.py`:

```python
    def test_skips_empty_translated_keeps_numbering_dense(self, tmp_path):
        segs = [
            _seg(0.0, 1.0, original="A.", translated="А."),
            _seg(1.0, 2.0, original="B.", translated=""),  # пропускается
            _seg(2.0, 3.0, original="C.", translated="В."),
        ]
        path = tmp_path / "out.ru.srt"
        n = write_srt(segs, str(path), lang="ru")
        assert n == 2
        content = path.read_text(encoding="utf-8")
        # Numbering is 1, 2 (no gap from skipped segment)
        assert content.startswith("1\n")
        assert "\n2\n" in content
        assert "\n3\n" not in content

    def test_skips_whitespace_only_text(self, tmp_path):
        segs = [
            _seg(0.0, 1.0, original="A."),
            _seg(1.0, 2.0, original="   \n  "),  # whitespace only
        ]
        path = tmp_path / "out.en.srt"
        n = write_srt(segs, str(path), lang="en")
        assert n == 1

    def test_skips_invalid_timing_zero_duration(self, tmp_path):
        segs = [
            _seg(0.0, 1.0, original="A."),
            _seg(1.0, 1.0, original="B."),  # zero duration
            _seg(2.0, 3.0, original="C."),
        ]
        path = tmp_path / "out.en.srt"
        n = write_srt(segs, str(path), lang="en")
        assert n == 2

    def test_skips_invalid_timing_end_before_start(self, tmp_path, capsys):
        segs = [
            _seg(0.0, 1.0, original="A."),
            _seg(2.0, 1.5, original="B."),  # end < start
        ]
        path = tmp_path / "out.en.srt"
        n = write_srt(segs, str(path), lang="en")
        assert n == 1
        captured = capsys.readouterr()
        assert "[subtitles]" in captured.err
        assert "end < start" in captured.err

    def test_empty_segments_creates_empty_file(self, tmp_path):
        path = tmp_path / "out.en.srt"
        n = write_srt([], str(path), lang="en")
        assert n == 0
        assert path.exists()
        assert path.read_text(encoding="utf-8") == ""
```

- [ ] **Step 2: Run чтобы убедиться что часть тестов падает**

Run: `uv run pytest tests/test_subtitles.py::TestWriteSrt -v`
Expected: первые 3 теста PASS, 5 новых FAIL (текущая реализация пишет всё подряд без проверок).

- [ ] **Step 3: Дописать skip-логику в `write_srt`**

Заменить тело `write_srt` в `src/subtitles.py` на:

```python
def write_srt(
    segments: list[Segment], path: str, lang: Literal["en", "ru"]
) -> int:
    """Write `segments` as SRT to `path`. Returns count of cues written.

    `lang="en"` uses seg.original; `lang="ru"` uses seg.translated.
    Skips segments with empty/whitespace text or invalid timing
    (start >= end). Numbering is sequential over written cues only.
    Existing files at `path` are overwritten.
    """
    count = 0
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments):
            if seg.end < seg.start:
                print(
                    f"[subtitles] skip: end < start at idx {i} "
                    f"({seg.start} → {seg.end})",
                    file=sys.stderr,
                )
                continue
            if seg.start >= seg.end:
                continue
            raw = seg.original if lang == "en" else seg.translated
            text = _wrap(_escape(raw))
            if not text:
                continue
            count += 1
            f.write(f"{count}\n")
            f.write(f"{_format_timecode(seg.start)} --> {_format_timecode(seg.end)}\n")
            f.write(f"{text}\n\n")
    return count
```

И добавить импорт в начало `src/subtitles.py`:

```python
import sys
```

- [ ] **Step 4: Run всех тестов модуля**

Run: `uv run pytest tests/test_subtitles.py -v`
Expected: все тесты PASS (TestFormatTimecode×5, TestWrap×4, TestEscape×5, TestWriteSrt×8 = 22).

- [ ] **Step 5: Полный прогон test suite**

Run: `uv run pytest`
Expected: все тесты проекта PASS (старые + 22 новых).

- [ ] **Step 6: Commit**

```bash
git add src/subtitles.py tests/test_subtitles.py
git commit -m "feat(subtitles): skip empty/invalid segments with dense numbering"
```

---

### Task 7: Wire-up в `src/dub.py`

**Files:**
- Modify: `src/dub.py`

- [ ] **Step 1: Добавить импорт**

В `src/dub.py` после строки `from tts import synthesize` добавить:

```python
from subtitles import write_srt
```

- [ ] **Step 2: Поменять счётчики шагов с `[N/4]` на `[N/5]`**

В функции `main()` заменить:
- `[1/4] Transcribing...` → `[1/5] Transcribing...`
- `[2/4] Translating...` → `[2/5] Translating...`
- `[3/4] Synthesizing speech...` → `[3/5] Synthesizing speech...`
- `[4/4] Merging audio...` → `[4/5] Merging audio...`

- [ ] **Step 3: Добавить шаг `[5/5]` после `merge()`**

Заменить блок:

```python
    print("[4/5] Merging audio...")
    output = merge(video_path, segments, config["output"]["suffix"])

    print(f"\nDone! Output saved to: {output}")
```

на:

```python
    print("[4/5] Merging audio...")
    output = merge(video_path, segments, config["output"]["suffix"])

    print("[5/5] Writing subtitles...")
    out = Path(output)
    en_srt = out.with_suffix(".en.srt")
    ru_srt = out.with_suffix(".ru.srt")
    en_count = write_srt(segments, str(en_srt), lang="en")
    ru_count = write_srt(segments, str(ru_srt), lang="ru")
    print(f"      {en_srt.name}: {en_count} cues, {ru_srt.name}: {ru_count} cues")

    print(f"\nDone! Output saved to: {output}")
```

(`Path` уже импортирован в `dub.py`.)

- [ ] **Step 4: Добавить мок `write_srt` в `tests/test_dub.py`**

Без этого `test_main_full_pipeline` запустит настоящий writer и создаст файлы `/tmp/video_dubbed.{en,ru}.srt` (тест пройдёт, но оставит мусор и нарушит изоляцию).

В `tests/test_dub.py` найти декораторы `test_main_full_pipeline`:

```python
@patch("dub.merge")
@patch("dub.synthesize")
@patch("dub.translate")
@patch("dub.transcribe")
@patch("dub.check_prerequisites")
@patch("dub.load_config")
@patch("pathlib.Path.exists", return_value=True)
def test_main_full_pipeline(
    mock_exists,
    mock_config,
    mock_check,
    mock_transcribe,
    mock_translate,
    mock_synthesize,
    mock_merge,
):
```

Добавить `@patch("dub.write_srt")` ПЕРЕД `@patch("dub.merge")` (декораторы применяются bottom-up, но в сигнатуре mocks идут в обратном порядке относительно стека `@patch`):

```python
@patch("dub.write_srt")
@patch("dub.merge")
@patch("dub.synthesize")
@patch("dub.translate")
@patch("dub.transcribe")
@patch("dub.check_prerequisites")
@patch("dub.load_config")
@patch("pathlib.Path.exists", return_value=True)
def test_main_full_pipeline(
    mock_exists,
    mock_config,
    mock_check,
    mock_transcribe,
    mock_translate,
    mock_synthesize,
    mock_merge,
    mock_write_srt,
):
    mock_config.return_value = FAKE_CONFIG
    mock_transcribe.return_value = FAKE_SEGMENTS
    mock_translate.return_value = FAKE_SEGMENTS
    mock_synthesize.return_value = FAKE_SEGMENTS
    mock_merge.return_value = "/tmp/video_dubbed.mp4"
    mock_write_srt.return_value = 1
```

(Параметр `mock_write_srt` добавляется в самый конец списка — он соответствует САМОМУ ВЕРХНЕМУ `@patch`. См. документацию `unittest.mock.patch` "When used as a class decorator… the order of decorators is reversed.")

- [ ] **Step 5: Run test_dub**

Run: `uv run pytest tests/test_dub.py -v`
Expected: 3 PASS.

- [ ] **Step 6: Полный прогон**

Run: `uv run pytest`
Expected: всё PASS, никаких файлов в `/tmp/` после прогона (`ls /tmp/video_dubbed*` → empty).

- [ ] **Step 7: Commit**

```bash
git add src/dub.py tests/test_dub.py
git commit -m "feat(dub): wire SRT subtitle writer after merge"
```

---

### Task 8: Прогон на реальном видео + отчёт

**Files:**
- Create: `experiments/results/2026-05-03-srt-subtitles.md`

- [ ] **Step 1: Выбрать видео из `data/`**

Run: `ls data/*.mp4 | head -5`
Выбрать одно короткое (3–10 минут предпочтительно — быстрее прогон). Если нет короткого — взять любое уже-обработанное (для которого `_dubbed.mp4` уже существует — тогда полный прогон всё равно нужен, потому что у нас новый шаг; но Ollama / faster-whisper кешей нет, прогон полный).

- [ ] **Step 2: Убедиться что Ollama запущена**

Run: `curl -s http://localhost:11434/api/tags | head -c 100`
Expected: JSON с моделями. Если не отвечает — `ollama serve` в отдельном терминале.

- [ ] **Step 3: Запустить пайплайн**

Run: `uv run src/dub.py "data/<chosen-video>.mp4" 2>&1 | tee /tmp/srt-run.log`
Expected: пайплайн отработал, последний шаг `[5/5] Writing subtitles...` напечатал `<video>_dubbed.en.srt: N cues, <video>_dubbed.ru.srt: M cues`.

- [ ] **Step 4: Проверить наличие и базовую валидность файлов**

```bash
ls -la "data/<chosen-video>_dubbed".{mp4,en.srt,ru.srt}
head -20 "data/<chosen-video>_dubbed.en.srt"
head -20 "data/<chosen-video>_dubbed.ru.srt"
```

Expected: оба `.srt` существуют, размер > 0, в начале корректный cue-блок (`1\n00:00:..,... --> ..\n<text>\n\n`).

- [ ] **Step 5: Парсинг через `pysrt` для валидации**

```bash
uv pip install pysrt
uv run python -c "
import pysrt
en = pysrt.open('data/<chosen-video>_dubbed.en.srt')
ru = pysrt.open('data/<chosen-video>_dubbed.ru.srt')
print(f'EN: {len(en)} cues, last={en[-1].end}')
print(f'RU: {len(ru)} cues, last={ru[-1].end}')
"
```

Expected: pysrt парсит без exception, кол-во cue совпадает с тем что напечатал dub.py, last timecode разумен (≈ длина видео). `pysrt` ставится разово, не добавляем в `pyproject.toml`.

- [ ] **Step 6: Открыть видео в плеере (ручная проверка)**

Открыть `data/<chosen-video>_dubbed.mp4` в QuickTime (или VLC/mpv). В меню субтитров выбрать `English` или `Russian` — обе дорожки должны быть видны и подхватываться.

Сделать скриншот меню субтитров → сохранить в `experiments/results/2026-05-03-srt-subtitles-player.png` (опционально).

- [ ] **Step 7: Sanity по таймингам**

В плеере перейти на 5–10 случайных временных меток, сверить: что слышно в дубляже на этой секунде ≈ что написано в `.ru.srt` cue, активном в этот момент. Расхождения в пределах ±0.3 сек — норма (resegmenter границы).

Записать в отчёт сводку: «5 проверенных меток, расхождения в пределах ±X сек, явных рассинхронов нет / есть на меток N, M».

- [ ] **Step 8: Написать отчёт `experiments/results/2026-05-03-srt-subtitles.md`**

```markdown
# SRT sidecar subtitles — реализация и smoke-тест

Дата: 2026-05-03
Spec: `docs/superpowers/specs/2026-05-03-srt-subtitles-design.md`
Plan: `docs/superpowers/plans/2026-05-03-srt-subtitles.md`
Ветка: `feature/srt-subtitles`

## Setup

- Видео: `data/<chosen-video>.mp4` (длительность ~X мин).
- Прогон: `uv run src/dub.py data/<chosen-video>.mp4`.
- Конфиг: `config.yaml` без изменений.

## Артефакты

| Файл | Размер | Cues |
|---|---|---|
| `<chosen-video>_dubbed.mp4` | XXX MB | — |
| `<chosen-video>_dubbed.en.srt` | XX KB | N |
| `<chosen-video>_dubbed.ru.srt` | XX KB | M |

(`N` и `M` могут отличаться — `.ru.srt` пропускает сегменты с пустым `translated`.)

## Валидация

1. **Парсинг pysrt:** оба файла парсятся без ошибок. Last timecode EN=…, RU=… — сходится с длительностью видео.
2. **Player autoload:** QuickTime автоматически подхватил обе дорожки субтитров. Скриншот меню — `experiments/results/2026-05-03-srt-subtitles-player.png` (если приложен).
3. **Тайминги:** 5 случайных меток сверены с слышимым звуком — расхождения ≤ X сек, явных рассинхронов нет.

## Verdict

Sidecar SRT работают как ожидалось. Фича готова к merge в main.

## Что НЕ сделано (намеренно, out of scope)

- Soft-subs / hard-subs внутрь mp4 (#14 варианты B/C) — отложены до явного запроса.
- Сплит длинных cue по таймингу — текущий `.ru.srt` на боевом видео читаемый, оверкилл не нужен.
```

- [ ] **Step 9: Commit отчёта**

```bash
git add experiments/results/2026-05-03-srt-subtitles.md
# если есть скриншот:
# git add experiments/results/2026-05-03-srt-subtitles-player.png
git commit -m "experiment(srt-subtitles): smoke run on <chosen-video>"
```

---

### Task 9: Закрыть пункт #14 в backlog'е

**Files:**
- Modify: `docs/dubbing-improvements.md`

- [ ] **Step 1: Добавить Status-блок под заголовком #14**

В `docs/dubbing-improvements.md` найти строку `#### 14. SRT subtitle generation — _open-dubbing/subtitles.py_` и сразу под ней (перед строкой `**Сложность: 10/100 · Эффект: 25/100**`) вставить:

```markdown
> **Status (2026-05-03):** Реализовано в варианте A (sidecar-only). Два `.srt` файла рядом с output mp4, плеер автоподхватывает по совпадающему стему. Отчёт — `experiments/results/2026-05-03-srt-subtitles.md`. Варианты B (soft-subs muxed) и C (hard-subs burn-in) отложены до явного запроса. Реактивировать B/C, если: (а) нужна доставка одним файлом без sidecar; (б) hard-subs для соцсетей/мессенджеров без поддержки внешних треков.
```

- [ ] **Step 2: Зачеркнуть в Фазе 1 «Рекомендуемого порядка»**

В разделе `### Фаза 1 — самые дешёвые победы` найти строку:

```markdown
4. **#14 SRT subtitle generation** (10 / 25). ~30 строк кода, заметная UX-фича.
```

Заменить на:

```markdown
4. ~~**#14 SRT subtitle generation** (10 / 25).~~ **Сделано** (2026-05-03): sidecar `.en.srt` + `.ru.srt`, новый `src/subtitles.py`. См. `experiments/results/2026-05-03-srt-subtitles.md`.
```

- [ ] **Step 3: Diff и commit**

Run: `git diff docs/dubbing-improvements.md`
Expected: ровно две правки в указанных местах, ничего лишнего.

```bash
git add docs/dubbing-improvements.md
git commit -m "docs(srt-subtitles): mark #14 as done in backlog"
```

---

### Task 10: Финализация — push + merge

**Files:** —

- [ ] **Step 1: Полный прогон тестов на ветке**

Run: `uv run pytest`
Expected: всё PASS.

- [ ] **Step 2: Свод изменений на ветке**

Run: `git log --oneline main..HEAD`
Expected: ~7 коммитов в порядке: timecode → wrap → escape → write_srt happy → write_srt edge → wire-up dub → smoke report → backlog mark.

- [ ] **Step 3: Запросить решение у пользователя**

Спросить: merge через PR (`gh pr create`) или прямой fast-forward в main (`git checkout main && git merge feature/srt-subtitles`)? Не делать ни того, ни другого без явного «да».

- [ ] **Step 4: После одобрения merge — удалить worktree**

```bash
cd /Users/nbirukov/Courses/vt-claude
git worktree remove ../vt-claude-srt-subtitles
git branch -d feature/srt-subtitles  # после merge
```
