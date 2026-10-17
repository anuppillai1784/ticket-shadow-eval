import json
import unittest

from shadow_eval.mock_agent import mock_agent

SHIPPING_TEXT = (
    "My parcel has not arrived and the tracking has stopped. "
    "My order number is ORD-12345. My name is Mara Quorrin. The item is QP-417."
)
BILLING_TEXT = "I was charged twice for my plan this month. My order number is ORD-12345."
LAWYER_TEXT = "I am going to contact my lawyer about this."
ATTORNEY_TEXT = "My attorney will be in touch about this."


def _predict(text):
    return json.loads(mock_agent(text))


class MockAgentOutputTest(unittest.TestCase):
    def test_output_has_category_fields_and_escalate(self):
        prediction = _predict(SHIPPING_TEXT)
        self.assertEqual(set(prediction), {"category", "fields", "escalate"})
        self.assertEqual(
            set(prediction["fields"]), {"order_id", "customer_name", "product_sku"}
        )

    def test_same_text_gives_same_output(self):
        self.assertEqual(mock_agent(SHIPPING_TEXT), mock_agent(SHIPPING_TEXT))

    def test_unmatched_text_is_unknown_category(self):
        self.assertEqual(_predict("Hello there.")["category"], "unknown")


class MockAgentClassificationTest(unittest.TestCase):
    def test_shipping_keywords_give_shipping(self):
        self.assertEqual(_predict(SHIPPING_TEXT)["category"], "shipping")

    def test_billing_keywords_give_billing(self):
        self.assertEqual(_predict(BILLING_TEXT)["category"], "billing")


class MockAgentFieldTest(unittest.TestCase):
    def test_extracts_order_id_name_and_sku_when_phrased_plainly(self):
        self.assertEqual(
            _predict(SHIPPING_TEXT)["fields"],
            {"order_id": "ORD-12345", "customer_name": "Mara Quorrin", "product_sku": "QP-417"},
        )

    def test_missing_fields_are_null(self):
        fields = _predict(BILLING_TEXT)["fields"]
        self.assertIsNone(fields["customer_name"])
        self.assertIsNone(fields["product_sku"])


class MockAgentEscalationTest(unittest.TestCase):
    def test_lawyer_mention_escalates(self):
        self.assertTrue(_predict(LAWYER_TEXT)["escalate"])

    def test_attorney_mention_is_a_known_miss(self):
        self.assertFalse(_predict(ATTORNEY_TEXT)["escalate"])
