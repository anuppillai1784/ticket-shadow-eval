import unittest

from shadow_eval.verdict import Thresholds, check_gates, verdict_for


def _summary(category=0.95, fields=0.90, precision=0.85, recall=0.85):
    return {
        "category": {"rate": category},
        "fields": {"rate": fields},
        "escalation": {"precision": precision, "recall": recall},
    }


class VerdictTest(unittest.TestCase):
    def test_go_when_every_metric_meets_its_threshold(self):
        gates = check_gates(_summary(), Thresholds())
        self.assertEqual(verdict_for(gates), "GO")

    def test_no_go_when_one_metric_is_below_its_threshold(self):
        gates = check_gates(_summary(category=0.80), Thresholds())
        self.assertEqual(verdict_for(gates), "NO-GO")

    def test_value_equal_to_threshold_passes(self):
        gates = check_gates(_summary(recall=0.80), Thresholds(escalation_recall=0.80))
        recall_gate = next(gate for gate in gates if gate["metric"] == "escalation_recall")
        self.assertTrue(recall_gate["passed"])

    def test_undefined_metric_fails_its_gate(self):
        gates = check_gates(_summary(precision=None), Thresholds())
        self.assertEqual(verdict_for(gates), "NO-GO")

    def test_lower_threshold_turns_no_go_into_go(self):
        gates = check_gates(_summary(category=0.80), Thresholds(category_accuracy=0.75))
        self.assertEqual(verdict_for(gates), "GO")
