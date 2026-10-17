import json
import unittest

from shadow_eval.parse import parse_prediction

VALID_PREDICTION = {
    "category": "billing",
    "fields": {"order_id": None, "customer_name": None, "product_sku": None},
    "escalate": False,
}


class ParsePredictionTest(unittest.TestCase):
    def test_valid_prediction_is_returned(self):
        self.assertEqual(parse_prediction(json.dumps(VALID_PREDICTION)), VALID_PREDICTION)

    def test_invalid_json_gives_none(self):
        self.assertIsNone(parse_prediction("category: billing"))

    def test_json_that_is_not_an_object_gives_none(self):
        self.assertIsNone(parse_prediction("[1, 2, 3]"))

    def test_object_missing_a_required_key_gives_none(self):
        partial = {key: value for key, value in VALID_PREDICTION.items() if key != "escalate"}
        self.assertIsNone(parse_prediction(json.dumps(partial)))
