import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from taskmate.cli import main




print("hello this is the beginning")
def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = str(Path(self.tmp.name) / "tasks.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_then_list(self):
        code, out, _ = run("--file", self.file, "add", "Buy milk", "--priority", "high")
        self.assertEqual(code, 0)
        self.assertIn("added:", out)
        _, out, _ = run("--file", self.file, "list")
        self.assertIn("#1 Buy milk <high>", out)

    def test_done_missing_task_returns_error(self):
        code, _, err = run("--file", self.file, "done", "42")
        self.assertEqual(code, 1)
        self.assertIn("no task with id 42", err)

    def test_search(self):
        run("--file", self.file, "add", "Learn git")
        run("--file", self.file, "add", "Cook dinner")
        _, out, _ = run("--file", self.file, "search", "git")
        self.assertIn("Learn git", out)
        self.assertNotIn("Cook dinner", out)


if __name__ == "__main__":
    unittest.main()
