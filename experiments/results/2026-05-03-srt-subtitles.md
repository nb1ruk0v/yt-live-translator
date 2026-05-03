# SRT sidecar subtitles — реализация и smoke-тест

Дата: 2026-05-03
Spec: `docs/superpowers/specs/2026-05-03-srt-subtitles-design.md`
Plan: `docs/superpowers/plans/2026-05-03-srt-subtitles.md`
Ветка: `feature/srt-subtitles`

## Setup

- Видео: `data/Prompting for Agents.mp4` (29:30, 72 MB).
- Прогон: `uv run src/dub.py "data/Prompting for Agents.mp4"`.
- Конфиг: `config.yaml` без изменений (`gemma4:e4b`, `kseniya`, `whisper turbo`).
- Длительность прогона: ~15 минут (CPU). Transcribe ~7 мин (turbo+int8, ~4× realtime), остальные шаги ~8 мин совокупно.

## Артефакты

| Файл | Размер | Cues |
|---|---|---|
| `Prompting for Agents_dubbed.mp4` | 109 MB | — |
| `Prompting for Agents_dubbed.en.srt` | 26 KB | 240 |
| `Prompting for Agents_dubbed.ru.srt` | 40 KB | 240 |

EN/RU cue counts равны (фолбэков в пустые переводы не было). Соотношение размеров `40/26 ≈ 1.54` соответствует типичному 50% расширению русского текста относительно английского.

Из лога merge: `156/240` сегментов потребовали atempo-стрейч, суммарно `3.71s` обрезано atempo-cap'ом. Это базовый профиль для русского дубляжа без compaction-pass'а (#2 в backlog).

## Валидация

### 1. Парсинг pysrt

```python
import pysrt
en = pysrt.open('data/Prompting for Agents_dubbed.en.srt')  # 240 cues, 00:00:05,230 → 00:29:23,170
ru = pysrt.open('data/Prompting for Agents_dubbed.ru.srt')  # 240 cues, 00:00:05,230 → 00:29:23,170
```

Оба файла парсятся без exception. Тайминги первого и последнего cue идентичны в обоих языках (это инвариант: тайминги берутся из `Segment.start/end`, перевод не сдвигает границы).

### 2. Player autoload

QuickTime / VLC / mpv: открыть `Prompting for Agents_dubbed.mp4` → в меню субтитров видны обе дорожки (`<filename>.en.srt`, `<filename>.ru.srt`), переключаются. Подтверждено пользователем (4/4 пункта проверки).

### 3. Sanity таймингов

Случайные временные метки → cue в `.ru.srt` совпадает с тем, что слышно в дубляже на этой секунде. Явных рассинхронов не наблюдается. Подтверждено пользователем.

### 4. Примеры cue

```
1
00:00:05,230 --> 00:00:11,330
All right, thank you. Thank you, everyone,
for joining us. So we're picking up with…

1
00:00:05,230 --> 00:00:11,330
Спасибо всем, что присоединились. Итак,
переходим к промптингу для агентов.
```

```
100
00:12:31,250 --> 00:12:34,150
And so they might take these web results
and run with them immediately.

100
00:12:31,250 --> 00:12:34,150
И поэтому они могут взять эти веб-
результаты и сразу же начать с ними…
```

Видны (а) wrap до 2 строк ≤42 символов, (б) overflow truncation с `…` на длинных предложениях, (в) `textwrap` иногда ломает после дефиса (`веб-/результаты`) — косметически не идеально, но не баг.

## Verdict

Sidecar SRT работают как ожидалось. Файлы валидны, плеер автоподхватывает обе дорожки, тайминги согласованы со звуком. Фича готова к merge в main.

## Что НЕ сделано (намеренно, out of scope)

- **Soft-subs** (`-c:s mov_text`) и **hard-subs** (burn-in) внутрь mp4 — варианты B/C из обсуждения. Откладываются до явного запроса (нужна доставка одним файлом без sidecar или hard-subs для соцсетей).
- Сплит длинных cue по таймингу (вариант C cue-маппинга) — на боевом видео `.ru.srt` читаемый, `…` truncation встречается на ~10-20% cue, не «стена текста». Оверкилл не нужен.
- Конфигурируемые `width`/`max_lines` — захардкожены 42/2 (стандарт SRT). Вынести в `config.yaml` имеет смысл только если появятся реальные кейсы под другую читаемость.
