from dataclasses import dataclass, field


@dataclass
class Segment:
    start: float
    end: float
    original: str
    translated: str = field(default="")
    audio_path: str = field(default="")
