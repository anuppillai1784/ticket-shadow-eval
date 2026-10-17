import random
import unittest

from shadow_eval.model import CATEGORIES, FIELD_NAMES
from shadow_eval.tickets import generate_tickets, swap_adjacent_letters

SEED = 7
TICKET_COUNT = 100


class GenerateTicketsTest(unittest.TestCase):
    def setUp(self):
        self.tickets = generate_tickets(SEED)

    def test_generates_one_hundred_tickets_with_unique_ids(self):
        ids = [ticket["id"] for ticket in self.tickets]
        self.assertEqual(len(self.tickets), TICKET_COUNT)
        self.assertEqual(len(set(ids)), TICKET_COUNT)

    def test_same_seed_gives_same_tickets(self):
        self.assertEqual(generate_tickets(SEED), self.tickets)

    def test_different_seed_gives_different_tickets(self):
        self.assertNotEqual(generate_tickets(SEED + 1), self.tickets)

    def test_categories_are_balanced(self):
        counts = {category: 0 for category in CATEGORIES}
        for ticket in self.tickets:
            counts[ticket["truth"]["category"]] += 1
        self.assertEqual(set(counts.values()), {TICKET_COUNT // len(CATEGORIES)})

    def test_truth_has_category_fields_and_escalate(self):
        for ticket in self.tickets:
            truth = ticket["truth"]
            self.assertIn(truth["category"], CATEGORIES)
            self.assertIsInstance(truth["escalate"], bool)
            self.assertEqual(set(truth["fields"]), set(FIELD_NAMES))

    def test_order_id_appears_in_text_only_when_present(self):
        for ticket in self.tickets:
            has_order_id = ticket["truth"]["fields"]["order_id"] is not None
            self.assertEqual("ORD-" in ticket["text"], has_order_id)

    def test_some_fields_are_missing_and_some_tickets_escalate(self):
        fields = [ticket["truth"]["fields"] for ticket in self.tickets]
        self.assertTrue(any(f["customer_name"] is None for f in fields))
        self.assertTrue(any(ticket["truth"]["escalate"] for ticket in self.tickets))
        self.assertTrue(any(not ticket["truth"]["escalate"] for ticket in self.tickets))


class SwapAdjacentLettersTest(unittest.TestCase):
    def test_swaps_two_neighbouring_letters_and_keeps_length(self):
        typo = swap_adjacent_letters("refund", random.Random(1))
        self.assertNotEqual(typo, "refund")
        self.assertEqual(len(typo), len("refund"))
        self.assertEqual(sorted(typo), sorted("refund"))
