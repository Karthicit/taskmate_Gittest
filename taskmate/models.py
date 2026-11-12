"""Data model for TaskMate."""
from dataclasses import asdict, dataclass
from typing import Optional

PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False
    due: Optional[str] = None  # ISO date string, e.g. "2026-12-31"

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        if self.priority not in PRIORITIES:
            raise ValueError(f"priority must be one of {PRIORITIES}")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(**data)
