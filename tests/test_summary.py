import unittest

from shadow_eval.model import FIELD_NAMES
from shadow_eval.scoring import score_record
from shadow_eval.stats import wilson_interval
from shadow_eval.summary import summarize


def _row(human_category, agent_category, human_escalate=False, flagged=False, matches=3):
    human = {
        "category": human_category,
        "fields": {name: "value" for name in FIELD_NAMES},
        "escalate": human_escalate,
    }
    agent_fields = {
        name: "value" if index < matches else "other" for index, name in enumerate(FIELD_NAMES)
    }
    agent = {"category": agent_category, "fields": agent_fields, "escalate": flagged}
    return _scored({"human": human, "agent": agent})


def _unparsed_row(human_category):
    human = {
        "category": human_category,
        "fields": {name: "value" for name in FIELD_NAMES},
        "escalate": False,
    }
    return _scored({"human": human, "agent": None})


def _scored(record):
    full = {"id": "T-001", "text": "ticket", "agent_raw": "", **record}
    return {**full, "score": score_record(full)}


class SummarizeCategoryTest(unittest.TestCase):
    def test_overall_category_rate_with_wilson_interval(self):
        rows = [
            _row("billing", "billing"),
            _row("billing", "billing"),
            _row("billing", "billing"),
            _row("billing", "refund"),
        ]
        category = summarize(rows)["category"]
        self.assertEqual((category["correct"], category["total"]), (3, 4))
        self.assertAlmostEqual(category["rate"], 0.75)
        low, high = wilson_interval(3, 4)
        self.assertAlmostEqual(category["low"], low)
        self.assertAlmostEqual(category["high"], high)

    def test_per_category_rates_only_for_present_categories(self):
        rows = [_row("billing", "billing"), _row("refund", "billing")]
        per_category = summarize(rows)["per_category"]
        self.assertEqual(set(per_category), {"billing", "refund"})
        self.assertAlmostEqual(per_category["billing"]["rate"], 1.0)
        self.assertAlmostEqual(per_category["refund"]["rate"], 0.0)


class SummarizeFieldTest(unittest.TestCase):
    def test_field_slots_are_counted_across_all_tickets(self):
        rows = [_row("billing", "billing", matches=2), _row("billing", "billing", matches=2)]
        fields = summarize(rows)["fields"]
        self.assertEqual((fields["correct"], fields["total"]), (4, 6))


class SummarizeEscalationTest(unittest.TestCase):
    def test_confusion_counts_precision_and_recall(self):
        rows = [
            _row("billing", "billing", human_escalate=True, flagged=True),
            _row("billing", "billing", human_escalate=True, flagged=False),
            _row("billing", "billing", human_escalate=False, flagged=True),
            _row("billing", "billing"),
            _row("billing", "billing"),
        ]
        escalation = summarize(rows)["escalation"]
        self.assertEqual(
            (escalation["true_positive"], escalation["false_negative"]), (1, 1)
        )
        self.assertEqual(
            (escalation["false_positive"], escalation["true_negative"]), (1, 2)
        )
        self.assertAlmostEqual(escalation["precision"], 0.5)
        self.assertAlmostEqual(escalation["recall"], 0.5)

    def test_precision_is_none_when_nothing_is_flagged(self):
        rows = [_row("billing", "billing", human_escalate=True)]
        escalation = summarize(rows)["escalation"]
        self.assertIsNone(escalation["precision"])
        self.assertAlmostEqual(escalation["recall"], 0.0)

    def test_recall_is_none_when_no_ticket_should_escalate(self):
        rows = [_row("billing", "billing", flagged=True)]
        escalation = summarize(rows)["escalation"]
        self.assertIsNone(escalation["recall"])
        self.assertAlmostEqual(escalation["precision"], 0.0)


class SummarizeEdgeCaseTest(unittest.TestCase):
    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            summarize([])

    def test_unparsed_output_is_counted_as_parse_failure(self):
        rows = [_row("billing", "billing"), _unparsed_row("billing")]
        summary = summarize(rows)
        self.assertEqual(summary["parse_failures"], 1)
        self.assertEqual(summary["category"]["correct"], 1)
