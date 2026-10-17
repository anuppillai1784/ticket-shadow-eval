import contextlib
import io
import os
import tempfile
import unittest

from shadow_eval.__main__ import main


class DeterminismTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = temp.name

    def _run(self, name, seed):
        out = os.path.join(self.root, name)
        with contextlib.redirect_stdout(io.StringIO()):
            main(["--seed", str(seed), "--out", out])
        return out

    def _read_bytes(self, out, name):
        with open(os.path.join(out, name), "rb") as handle:
            return handle.read()

    def test_same_seed_gives_identical_results_and_report(self):
        first = self._run("first", 7)
        second = self._run("second", 7)
        for name in ("results.jsonl", "report.md"):
            self.assertEqual(self._read_bytes(first, name), self._read_bytes(second, name))

    def test_different_seed_gives_different_results(self):
        first = self._run("first", 7)
        other = self._run("other", 8)
        self.assertNotEqual(
            self._read_bytes(first, "results.jsonl"), self._read_bytes(other, "results.jsonl")
        )
