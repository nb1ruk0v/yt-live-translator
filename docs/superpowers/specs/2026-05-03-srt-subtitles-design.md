# SRT subtitle generation — sidecar files

Дата: 2026-05-03
Backlog: пункт #14 из `docs/dubbing-improvements.md` (Фаза 1).

## Цель

После полного прогона `dub.py` сохранять рядом с output mp4 два sidecar-файла субтитров:

- `<output>.en.srt` — оригинал (`Segment.original`)
- `<output>.ru.srt` — перевод (`Segment.translated`)

Чтобы плеер (VLC, mpv, QuickTime) автоматически подхватывал их по совпадающему стему, и пользователь мог переключать дорожки EN/RU при просмотре дубляжа.

Это **UX/observability фича**, не качественный bench. Ничего в TTS/merge не изменяется, тайминги берутся as-is из `Segment.start/end`.

## Out of scope

- **Soft-subs** (`-c:s mov_text`) или **hard-subs** (burn-in) внутри mp4 — варианты B/C из обсуждения отложены. Если потребуется, добавляются позже как расширение `merge.py`, без касания `subtitles.py`.
- Word-level timestamps / karaoke-style highlighting (зависит от backlog #24).
- Сплит длинных сегментов на несколько cue по таймингу (вариант C из обсуждения cue-маппинга). При необходимости добавим, если на боевом видео `.srt` окажется нечитаем.
- Новые ключи в `config.yaml`. Поведение всегда-вкл, без флага.
- Записывать SRT при падении TTS или merge. Запись идёт после `merge()` по возвращаемому пути; падение upstream → нет sidecar (приемлемо: основная нагрузка — TTS, она к этому моменту уже прошла).

## Критерии успеха («реально ли помогло»)

Метрика бинарная — фича UX, числового прироста нет:

1. На одном видео из `data/` после `uv run src/dub.py <video>` появились `<video>_dubbed.en.srt` и `<video>_dubbed.ru.srt`, оба `cue_count > 0`.
2. **Парсинг.** Файлы валидны как SRT — проверить через `pysrt.open(path)` (или `ffprobe -i <video>_dubbed.mp4 -i <video>_dubbed.ru.srt` без ошибок). В отчёте — кол-во cue, размер файла.
3. **Player autoload.** Открыть `<video>_dubbed.mp4` в QuickTime/VLC/mpv → в меню субтитров видны обе дорожки EN и RU, переключаются. Скриншот в отчёт.
4. **Sanity таймингов.** Глазами пройтись по 5–10 случайным cue в `.ru.srt`, убедиться что таймкод ≈ совпадает с тем, что слышно в дубляже на этой секунде.

## Архитектура

```
src/
  subtitles.py             — write_srt() + helpers (новый, ~30–40 строк)
  dub.py                   — +3 строки после merge() для записи 2 sidecar файлов

tests/
  test_subtitles.py        — юнит-тесты writer'а

experiments/results/
  2026-05-03-srt-subtitles.md  — отчёт по DoD (cue counts, валидность, скриншот плеера)
```

Ничего не меняется в `transcribe.py`, `translate.py`, `tts.py`, `merge.py`, `segment.py`, `config.yaml`.

## API `src/subtitles.py`

```python
from typing import Literal
from segment import Segment

def write_srt(segments: list[Segment], path: str, lang: Literal["en", "ru"]) -> int:
    """Write segments as SRT to `path`. Returns number of cues written.

    `lang="en"` → seg.original; `lang="ru"` → seg.translated.
    Сегменты с пустым/whitespace текстом или невалидным таймингом пропускаются;
    нумерация cue остаётся сквозной без дыр.
    """
```

Private helpers:

- `_format_timecode(seconds: float) -> str` — `HH:MM:SS,mmm` (запятая, не точка). Округление до миллисекунд через `round(seconds * 1000)`.
- `_wrap(text: str, width: int = 42, max_lines: int = 2) -> str` — `textwrap.wrap(text, width)`, объединить первые `max_lines` строк через `\n`. Если строк больше `max_lines` — обрезать и добавить `…` в конец последней оставшейся строки.
- `_escape(text: str) -> str` — `strip()`, заменить внутренние `\n`/`\r` на пробел, заменить подстроку `-->` на `‐‐>` (en-dash, чтобы не сталкиваться с разделителем cue).

Кодировка файла: **UTF-8 без BOM**, перевод строк `\n` (LF). Финальная пустая строка после последнего cue (стандарт SRT).

### Формат cue

```
<n>
<HH:MM:SS,mmm> --> <HH:MM:SS,mmm>
<line 1, ≤42 chars>
<line 2, ≤42 chars, опционально>

```

Между cue — одна пустая строка. После последнего cue — тоже одна пустая строка (терминатор).

## Wire-up в `src/dub.py`

Добавляется после `merge()`, перед финальным `print`:

```python
print("[5/5] Writing subtitles...")
out = Path(output)
en_srt = out.with_suffix(".en.srt")
ru_srt = out.with_suffix(".ru.srt")
en_count = write_srt(segments, str(en_srt), lang="en")
ru_count = write_srt(segments, str(ru_srt), lang="ru")
print(f"      {en_srt.name}: {en_count} cues, {ru_srt.name}: {ru_count} cues")
```

Заголовки шагов меняются с `[N/4]` на `[N/5]`.

`Path(...).with_suffix(".en.srt")` заменяет последний суффикс на `.en.srt` → `test_video_dubbed.mp4` → `test_video_dubbed.en.srt`. Стем `test_video_dubbed` совпадает с видео — плеер автоподхватывает.

## Edge cases

| Случай | Поведение |
|---|---|
| `seg.translated == ""` (LLM-fallback не сработал) | В `.ru.srt` cue не пишется. В `.en.srt` тот же сегмент остаётся (там `original` непустой). |
| `seg.original == ""` (теоретически невозможен после resegmenter) | Пропускается в `.en.srt`. |
| Текст после `_escape` пустой (только whitespace) | Пропускается. |
| Текст длиннее `max_lines * width` после wrap | Обрезается до `max_lines` строк, в конец добавляется `…`. Без логирования (шум). |
| Внутренний `\n` в тексте | `_escape` → пробел до `_wrap`. |
| Подстрока `-->` в тексте | `_escape` → `‐‐>`. |
| `start == end` (нулевая длительность) | Пропускается. |
| `end < start` | Пропускается + warning в stderr (`[subtitles] skip: end < start at idx N`). |
| Список `segments` пустой | Файл создаётся пустым (0 байт), функция возвращает `0`. |

Сквозная нумерация **только для записанных** cue: пропуски не оставляют дыр (`1, 2, 3, ...`, не `1, 3, 5, ...`).

## Тесты `tests/test_subtitles.py`

| Тест | Что проверяет |
|---|---|
| `test_format_timecode_basic` | `0.0 → "00:00:00,000"`, `1.234 → "00:00:01,234"`, `3661.5 → "01:01:01,500"` |
| `test_format_timecode_milliseconds_round` | `0.9999 → "00:00:01,000"` (закрепить поведение `round`) |
| `test_wrap_short_text_single_line` | `"Hello world"` → одна строка, без `\n` |
| `test_wrap_long_text_two_lines` | Текст ~60 символов → 2 строки, каждая ≤42 |
| `test_wrap_overflow_truncates_with_ellipsis` | Текст ~200 символов → 2 строки, последняя оканчивается на `…` |
| `test_escape_arrow_replaced` | `"a-->b"` → `"a‐‐>b"` |
| `test_escape_internal_newlines_collapsed` | `"line1\nline2"` → `"line1 line2"` |
| `test_write_srt_basic_two_segments` | Snapshot: 2 валидных сегмента → ровно ожидаемая строка с `\n`-разделителями |
| `test_write_srt_skips_empty_translated` | Сегмент с `translated=""` не появляется в `.ru.srt`, нумерация остаётся сплошной |
| `test_write_srt_skips_invalid_timing` | `start >= end` → cue пропущен, returns корректный счётчик |
| `test_write_srt_returns_cue_count` | Функция возвращает число записанных cue (не общее число сегментов) |
| `test_write_srt_empty_segments_creates_empty_file` | Пустой список → файл создан, размер 0, returns `0` |

Не пишем: тестов на `Path.with_suffix` (стандартная библиотека), интеграционного теста с реальным видео (это покрывает DoD).

## Тонкости и риски

- **Стем output mp4.** `Path("test.mp4").with_suffix(".en.srt")` корректно даёт `test.en.srt`, но `Path("test.dubbed.mp4").with_suffix(".en.srt")` → `test.dubbed.en.srt` (заменяется только последний суффикс). С нашим `output.suffix: "_dubbed"` коллизий нет — суффикс приклеивается к стему, а не как `.dubbed`. Ок.
- **Кириллица в имени файла.** `<video>` после yt-dlp может содержать non-ASCII — `Path.with_suffix` это переживает, plain text запись через `open(..., 'w', encoding='utf-8')` тоже. Проверим в DoD.
- **Конфликт с существующими `.srt`.** Если рядом уже лежит `.en.srt` от прошлого прогона — перезаписываем без warning'а (как `merge.py` перезаписывает `_dubbed.mp4`). Документировать в docstring.
- **Длинные cue в `.ru.srt`.** Русский на 30–50% длиннее EN, поэтому RU чаще будет упираться в 2 строки × 42. Для дебаг-фичи приемлемо: edge-case truncation с `…` лучше, чем «стена», и встречается редко на хорошо нарезанных сегментах.
- **Терминальный `\n` в файле.** Стандарт SRT требует пустую строку после последнего cue. Закрепляем поведением: `f.write(cue + "\n")` для каждого cue, последний cue даёт `<text>\n\n` через стандартный шаблон. Покрыто snapshot-тестом.

## Последовательность работ

Будет конкретизирована в плане (`docs/superpowers/plans/`), но крупно:

1. Ветка `feature/srt-subtitles` (worktree).
2. `src/subtitles.py` + `tests/test_subtitles.py` — TDD: тесты сначала, реализация потом.
3. Wire-up в `src/dub.py`.
4. Прогон на одном видео из `data/`, сохранить артефакт в `experiments/results/2026-05-03-srt-subtitles.md` (cue counts, скриншот плеера, sanity-чек таймингов).
5. Обновить `docs/dubbing-improvements.md`: пункт #14 → `Status (2026-05-03): Сделано` со ссылкой на отчёт. Зачеркнуть в Фазе 1.
6. Merge в main.
