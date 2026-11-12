"""Business logic: the only layer that knows the rules."""
from typing import List, Optional

from .models import Task
from .storage import TaskStore


class TaskService:
    def __init__(self, store: Optional[TaskStore] = None):
        self.store = store or TaskStore()

    def add(self, title, priority="medium", due=None) -> Task:
        tasks = self.store.load()
        next_id = max((t.id for t in tasks), default=0) + 1
        task = Task(id=next_id, title=title, priority=priority, due=due)
        tasks.append(task)
        self.store.save(tasks)
        return task

    def list_tasks(self, show_done=True) -> List[Task]:
        tasks = self.store.load()
        if not show_done:
            tasks = [t for t in tasks if not t.done]
        return tasks

    def complete(self, task_id) -> Task:
        tasks = self.store.load()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                self.store.save(tasks)
                return task
        raise KeyError(f"no task with id {task_id}")

    def delete(self, task_id) -> None:
        tasks = self.store.load()
        remaining = [t for t in tasks if t.id != task_id]
        if len(remaining) == len(tasks):
            raise KeyError(f"no task with id {task_id}")
        self.store.save(remaining)

    def search(self, keyword) -> List[Task]:
        keyword = keyword.lower()
        return [t for t in self.store.load() if keyword in t.title.lower()]
