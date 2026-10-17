import unittest

from shadow_eval.pipeline import evaluate
from shadow_eval.report import failed_rows, render_report
from shadow_eval.summary import summarize
from shadow_eval.verdict import Thresholds, check_gates, verdict_for

SEED = 7


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.rows = evaluate(SEED)
        self.summary = summarize(self.rows)
        self.gates = check_gates(self.summary, Thresholds())
        self.verdict = verdict_for(self.gates)
        self.text = render_report(SEED, self.rows, self.summary, self.gates, self.verdict)

    def test_report_states_seed_and_verdict(self):
        self.assertIn(f"Seed: {SEED}", self.text)
        self.assertIn(f"Verdict: {self.verdict}", self.text)

    def test_report_lists_every_failed_ticket_and_no_passing_ticket(self):
        failing_ids = {row["id"] for row in failed_rows(self.rows)}
        self.assertTrue(failing_ids)
        for row in self.rows:
            listed = f"| {row['id']} |" in self.text
            self.assertEqual(listed, row["id"] in failing_ids, row["id"])

    def test_report_shows_wilson_interval_for_category_accuracy(self):
        self.assertIn("Wilson 95%", self.text)
        self.assertIn("| Category |", self.text)
