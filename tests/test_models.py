import unittest

from taskmate.models import Task


class TaskModelTests(unittest.TestCase):
    def test_defaults(self):
        task = Task(id=1, title="Buy milk")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.done)
        self.assertIsNone(task.due)

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            Task(id=1, title="   ")

    def test_bad_priority_rejected(self):
        with self.assertRaises(ValueError):
            Task(id=1, title="x", priority="urgent")

    def test_round_trip_dict(self):
        task = Task(id=2, title="Write report", priority="high", due="2026-12-01")
        self.assertEqual(Task.from_dict(task.to_dict()), task)


if __name__ == "__main__":
    unittest.main()
