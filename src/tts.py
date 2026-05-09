import contextlib
import os
import subprocess
import tempfile
import wave

from segment import Segment


def _wav_duration(path: str) -> float:
    with contextlib.closing(wave.open(path, "rb")) as w:
        frames = w.getnframes()
        rate = w.getframerate()
        return frames / float(rate) if rate else 0.0


def _write_silence(path: str, duration: float = 0.05, sample_rate: int = 24000) -> None:
    n_frames = int(duration * sample_rate)
    with contextlib.closing(wave.open(path, "wb")) as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(b"\x00\x00" * n_frames)


def _extract_reference(
    video_path: str,
    segments: list[Segment],
    target_seconds: float = 10.0,
    max_seconds: float = 15.0,
) -> str:
    if not segments:
        raise RuntimeError("Cannot extract XTTS reference: no segments")

    start = segments[0].start
    end = segments[-1].end
    for seg in segments:
        if seg.end - start >= target_seconds:
            end = min(seg.end, start + max_seconds)
            break

    out_path = os.path.splitext(video_path)[0] + "_ref.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-ss",
            f"{start:.3f}",
            "-to",
            f"{end:.3f}",
            "-ac",
            "1",
            "-ar",
            "22050",
            "-vn",
            out_path,
        ],
        check=True,
        capture_output=True,
    )
    return out_path


def _load_model(config: dict):
    from TTS.api import TTS

    model_name = config.get("model", "tts_models/multilingual/multi-dataset/xtts_v2")
    device = config.get("device", "cpu")
    return TTS(model_name=model_name, progress_bar=False).to(device)


def synthesize(segments: list[Segment], config: dict, video_path: str) -> list[Segment]:
    ref_path = _extract_reference(
        video_path,
        segments,
        target_seconds=config.get("reference_seconds", 10.0),
    )
    print(f"      Reference: {ref_path}")

    model = _load_model(config)
    language = config.get("language", "ru")

    for i, seg in enumerate(segments):
        out_path = os.path.join(tempfile.gettempdir(), f"seg_{i:04d}.wav")
        text = seg.translated.strip()

        if not text:
            _write_silence(out_path)
        else:
            model.tts_to_file(
                text=text,
                speaker_wav=ref_path,
                language=language,
                file_path=out_path,
            )

        seg.audio_path = out_path
        seg.audio_duration = _wav_duration(out_path)

    return segments
