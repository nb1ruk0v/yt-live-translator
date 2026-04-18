from dataclasses import dataclass, field


@dataclass
class Segment:
    start: float
    end: float
    original: str
    translated: str = field(default="")
    audio_path: str = field(default="")
    audio_duration: float = field(default=0.0)

    @property
    def duration(self) -> float:
        return self.end - self.start
