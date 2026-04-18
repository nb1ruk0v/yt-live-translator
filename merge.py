import ffmpeg
from pathlib import Path
from segment import Segment


ATEMPO_MAX = 1.25


def merge(video_path: str, segments: list[Segment], suffix: str) -> str:
    input_path = Path(video_path)
    output_path = input_path.with_name(f"{input_path.stem}{suffix}{input_path.suffix}")

    video = ffmpeg.input(video_path).video

    audio_streams = []
    overflow_count = 0
    truncated_total = 0.0
    for i, seg in enumerate(segments):
        stream = ffmpeg.input(seg.audio_path).audio

        if seg.duration > 0 and seg.audio_duration > seg.duration:
            ratio = seg.audio_duration / seg.duration
            tempo = min(ATEMPO_MAX, ratio)
            stretched = seg.audio_duration / tempo
            truncated = max(0.0, stretched - seg.duration)
            overflow_count += 1
            truncated_total += truncated
            print(
                f"      seg {i:3d}: audio {seg.audio_duration:5.2f}s > "
                f"window {seg.duration:5.2f}s, atempo={tempo:.2f}, "
                f"truncated {truncated:.2f}s"
            )
            stream = stream.filter("atempo", tempo)
            stream = stream.filter("atrim", duration=seg.duration)

        delay_ms = int(seg.start * 1000)
        stream = stream.filter("adelay", f"{delay_ms}|{delay_ms}")
        audio_streams.append(stream)

    if overflow_count:
        print(
            f"      {overflow_count}/{len(segments)} segments stretched, "
            f"{truncated_total:.2f}s total truncated"
        )

    if audio_streams:
        mixed = ffmpeg.filter(
            audio_streams, "amix", inputs=len(audio_streams), normalize=0
        )
        out = ffmpeg.output(video, mixed, str(output_path))
    else:
        out = ffmpeg.output(video, str(output_path))

    out.overwrite_output().run(capture_stdout=True, capture_stderr=True)
    return str(output_path)
