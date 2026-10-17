import unittest

from shadow_eval.scoring import score_record


def _truth(category="billing", order_id=None, name=None, sku=None, escalate=False):
    return {
        "category": category,
        "fields": {"order_id": order_id, "customer_name": name, "product_sku": sku},
        "escalate": escalate,
    }


def _prediction(category="billing", order_id=None, name=None, sku=None, escalate=False):
    return {
        "category": category,
        "fields": {"order_id": order_id, "customer_name": name, "product_sku": sku},
        "escalate": escalate,
    }


def _record(human, agent):
    return {"id": "T-001", "text": "ticket", "human": human, "agent_raw": "", "agent": agent}


class ScoreCategoryTest(unittest.TestCase):
    def test_matching_category_is_correct(self):
        score = score_record(_record(_truth("refund"), _prediction("refund")))
        self.assertTrue(score["category_correct"])

    def test_different_category_is_wrong(self):
        score = score_record(_record(_truth("refund"), _prediction("billing")))
        self.assertFalse(score["category_correct"])


class ScoreFieldTest(unittest.TestCase):
    def test_null_truth_matches_only_null_answer(self):
        score = score_record(_record(_truth(order_id=None), _prediction(order_id=None)))
        self.assertTrue(score["fields_correct"]["order_id"])

    def test_value_given_for_null_truth_is_wrong(self):
        score = score_record(_record(_truth(order_id=None), _prediction(order_id="ORD-1")))
        self.assertFalse(score["fields_correct"]["order_id"])

    def test_field_comparison_ignores_case_and_surrounding_spaces(self):
        score = score_record(
            _record(_truth(name="Mara Quorrin"), _prediction(name=" mara quorrin "))
        )
        self.assertTrue(score["fields_correct"]["customer_name"])


class ScoreEscalationTest(unittest.TestCase):
    def test_flag_and_expected_are_both_recorded(self):
        score = score_record(_record(_truth(escalate=True), _prediction(escalate=False)))
        self.assertFalse(score["escalate_flagged"])
        self.assertTrue(score["escalate_expected"])
        self.assertFalse(score["escalate_correct"])


class ScoreParseFailureTest(unittest.TestCase):
    def test_unparseable_output_scores_wrong_and_not_flagged(self):
        score = score_record(_record(_truth("refund", order_id="ORD-1", escalate=True), None))
        self.assertFalse(score["category_correct"])
        self.assertFalse(any(score["fields_correct"].values()))
        self.assertFalse(score["escalate_flagged"])
        self.assertTrue(score["parse_failed"])
