"""JSON file storage for tasks."""
import json
import os
from pathlib import Path
from typing import List

from .models import Task

DEFAULT_PATH = Path(os.environ.get("TASKMATE_FILE", Path.home() / ".taskmate.json"))


class TaskStore:
    def __init__(self, path=None):
        self.path = Path(path) if path else DEFAULT_PATH

    def load(self) -> List[Task]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [Task.from_dict(item) for item in json.load(f)]

    def save(self, tasks: List[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2)
