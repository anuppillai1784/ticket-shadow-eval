import contextlib
import io
import json
import os
import tempfile
import unittest

from shadow_eval.__main__ import main


class CliTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.out = os.path.join(temp.name, "out")

    def _run(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            code = main(["--out", self.out, *args])
        return code, printed.getvalue()

    def _read(self, name):
        with open(os.path.join(self.out, name), encoding="utf-8") as handle:
            return handle.read()

    def test_writes_one_json_row_per_ticket_and_a_report(self):
        code, _ = self._run("--seed", "7")
        rows = [json.loads(line) for line in self._read("results.jsonl").splitlines()]
        self.assertEqual(code, 0)
        self.assertEqual(len(rows), 100)
        self.assertIn("agent_raw", rows[0])
        self.assertIn("score", rows[0])
        self.assertIn("# Shadow evaluation report", self._read("report.md"))

    def test_prints_the_verdict(self):
        _, printed = self._run("--seed", "7")
        self.assertIn("Verdict: ", printed)

    def test_threshold_flag_sets_the_required_value_in_the_report(self):
        self._run("--seed", "7", "--min-category-accuracy", "0.5")
        category_row = next(
            line for line in self._read("report.md").splitlines()
            if line.startswith("| category_accuracy |")
        )
        self.assertIn("| 0.500 |", category_row)
