# Trim Silence Benchmark — Results

## From Vibe Coding to Agentic Engineering

| mode | Σ audio (s) | Δ vs none (%) | overflow | truncated (s) | avg trim (ms) |
|---|---:|---:|---:|---:|---:|
| none | 1751.09 | +0.00 | 114/244 | 2.90 | 0.0 |
| silero | 1748.18 | +0.17 | 113/244 | 2.90 | 11.9 |
| pydub | 1720.18 | +1.77 | 106/244 | 2.48 | 126.7 |
| ffmpeg | 1720.43 | +1.75 | 107/244 | 2.49 | 125.6 |
| numpy | 1720.16 | +1.77 | 108/244 | 2.49 | 126.8 |

### Per-segment trim divergence

| pair | mean abs diff (ms) | max abs diff (ms) |
|---|---:|---:|
| silero vs numpy | 119.25 ms | 518.00 ms |
| silero vs pydub | 119.14 ms | 518.00 ms |
| silero vs ffmpeg | 118.08 ms | 518.02 ms |
| numpy vs pydub | 6.83 ms | 32.50 ms |
| numpy vs ffmpeg | 5.53 ms | 28.75 ms |
| pydub vs ffmpeg | 4.16 ms | 41.48 ms |

## Mastering Claude Code in 30 minutes

| mode | Σ audio (s) | Δ vs none (%) | overflow | truncated (s) | avg trim (ms) |
|---|---:|---:|---:|---:|---:|
| none | 1566.62 | +0.00 | 124/260 | 2.60 | 0.0 |
| silero | 1563.43 | +0.20 | 124/260 | 2.45 | 12.3 |
| pydub | 1537.78 | +1.84 | 116/260 | 2.00 | 111.0 |
| ffmpeg | 1537.99 | +1.83 | 116/260 | 1.97 | 110.1 |
| numpy | 1537.54 | +1.86 | 116/260 | 1.98 | 111.9 |

### Per-segment trim divergence

| pair | mean abs diff (ms) | max abs diff (ms) |
|---|---:|---:|
| silero vs numpy | 99.71 ms | 205.00 ms |
| silero vs pydub | 98.76 ms | 210.00 ms |
| silero vs ffmpeg | 97.97 ms | 207.10 ms |
| numpy vs pydub | 6.79 ms | 45.00 ms |
| numpy vs ffmpeg | 5.60 ms | 42.52 ms |
| pydub vs ffmpeg | 4.15 ms | 45.90 ms |

## Prompting for Agents

| mode | Σ audio (s) | Δ vs none (%) | overflow | truncated (s) | avg trim (ms) |
|---|---:|---:|---:|---:|---:|
| none | 1897.20 | +0.00 | 156/240 | 3.71 | 0.0 |
| silero | 1893.85 | +0.18 | 156/240 | 3.71 | 13.9 |
| pydub | 1867.80 | +1.55 | 152/240 | 2.90 | 122.5 |
| ffmpeg | 1868.24 | +1.53 | 152/240 | 2.90 | 120.7 |
| numpy | 1868.18 | +1.53 | 152/240 | 2.90 | 120.9 |

### Per-segment trim divergence

| pair | mean abs diff (ms) | max abs diff (ms) |
|---|---:|---:|
| silero vs numpy | 110.84 ms | 374.00 ms |
| silero vs pydub | 112.47 ms | 379.00 ms |
| silero vs ffmpeg | 110.71 ms | 378.83 ms |
| numpy vs pydub | 5.79 ms | 40.00 ms |
| numpy vs ffmpeg | 4.95 ms | 20.02 ms |
| pydub vs ffmpeg | 3.74 ms | 33.44 ms |

## Conclusion

**Помогло ли?** — Маргинально.
- `Σ audio_duration` падает на **1.5–1.9%** — против обещанных в backlog 5–15%. На 31-минутном видео это ~30 секунд, размазанные по 240+ сегментам, < 0.1 с/сегмент.
- `truncated_total` падает с 2.6–3.7 с до 2.0–2.9 с — спасено суммарно ~0.8 секунды реальной речи на видео.
- `overflow_count` снижается на 3–5% (на 4–8 сегментов из 240–260).
- На `--listen "Prompting for Agents"` (видео с самым высоким overflow, 156/240 = 65%) **разница между всеми режимами на слух не различима**. None / silero / pydub / ffmpeg / numpy звучат одинаково.

Гипотеза про 100–400 мс хвостовой тишины в Silero TTS подтвердилась количественно (avg trim ~120 мс), но эта величина **не превращается в перцептивный эффект**: для overflow-сегментов atempo уже клампится в `ATEMPO_MAX=1.5`, и срезание 120 мс не переводит их в режим «помещается в окно».

**Идентичны ли A/B/C/D?** — Гипотеза автора частично подтверждена, частично опровергнута.
- numpy / pydub / ffmpeg: попарное расхождение **mean ~5 мс, max ~30–46 мс** на сегмент. На синтетике Silero они эквивалентны — выбор сводится к стоимости (numpy дешевле всех: zero new deps).
- Silero VAD vs остальные: **mean ~100–120 мс, max до 520 мс** расхождения. Silero VAD режет **в ~10 раз меньше** (avg 12 мс vs 120 мс). Он значительно консервативнее на TTS-выходе — видимо, считает «речью» хвостовое затухание, которое energy-threshold алгоритмы трактуют как тишину.

**Победитель.** **numpy** — если бы фичу решили интегрировать. Zero new dependencies, идентичен по результату pydub/ffmpeg, без subprocess-оверхеда.

**Слуховой sanity-check.** Из `--listen "Prompting for Agents"`: ни один режим не съел последний слог сегмента. Защитный лимит trim был не нужен.

**Рекомендация для backlog.** Понизить эффект пункта **#11 с 35/100 до 5–10/100**. Для текущего пайплайна (Silero TTS + en→ru через Ollama gemma) trim хвостовой тишины — net negative по cost/benefit: лишний код в `tts.py`, новые edge-cases (последний слог), а перцептивного выигрыша нет. Оставить инфраструктуру эксперимента (`experiments/trim_silence/`) на ветке `experiment/trim-silence-benchmark` как переиспользуемый каркас — пригодится при #10 (XTTS/F5 voice cloning) или #13 (Demucs vocal separation), где trim может стать актуальнее на записанной речи с шумом.
