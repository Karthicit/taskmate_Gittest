import tempfile
import unittest
from pathlib import Path

from taskmate.service import TaskService
from taskmate.storage import TaskStore


class TaskServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.service = TaskService(TaskStore(Path(self.tmp.name) / "tasks.json"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_assigns_incrementing_ids(self):
        first = self.service.add("one")
        second = self.service.add("two")
        self.assertEqual((first.id, second.id), (1, 2))

    def test_complete_marks_done(self):
        task = self.service.add("finish lab")
        self.service.complete(task.id)
        self.assertTrue(self.service.list_tasks()[0].done)

    def test_complete_missing_raises(self):
        with self.assertRaises(KeyError):
            self.service.complete(99)

    def test_delete_removes_task(self):
        task = self.service.add("temp")
        self.service.delete(task.id)
        self.assertEqual(self.service.list_tasks(), [])

    def test_pending_filter_hides_done(self):
        a = self.service.add("a")
        self.service.add("b")
        self.service.complete(a.id)
        titles = [t.title for t in self.service.list_tasks(show_done=False)]
        self.assertEqual(titles, ["b"])

    def test_search_is_case_insensitive(self):
        self.service.add("Learn GIT branching")
        self.service.add("Buy milk")
        found = self.service.search("git")
        self.assertEqual([t.title for t in found], ["Learn GIT branching"])


if __name__ == "__main__":
    unittest.main()
