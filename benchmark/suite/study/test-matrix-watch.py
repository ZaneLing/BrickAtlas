"""CPU-only regression for watcher locking, without loading the training stack."""
import fcntl
import importlib
from pathlib import Path
import tempfile
import unittest

watch = importlib.import_module("follow-matrix")


class WatchTests(unittest.TestCase):
    def test_exact_matrix(self):
        self.assertEqual(len(watch.EXPECTED), 10)
        self.assertEqual(len(set(watch.EXPECTED)), 10)
        self.assertIn("leave-edit-seed43", watch.EXPECTED)
        self.assertNotIn("base-seed29", watch.EXPECTED)

    def test_running_uses_lock_not_stale_pid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertFalse(watch.matrix_running(root))
            with (root / "matrix.lock").open("a") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self.assertTrue(watch.matrix_running(root))
            self.assertFalse(watch.matrix_running(root))


if __name__ == "__main__":
    unittest.main()
