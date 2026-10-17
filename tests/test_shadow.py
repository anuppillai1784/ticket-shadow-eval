import unittest

from shadow_eval.shadow import run_shadow

TICKETS = [
    {
        "id": "T-001",
        "text": "first ticket",
        "truth": {
            "category": "billing",
            "fields": {"order_id": None, "customer_name": None, "product_sku": None},
            "escalate": False,
        },
    },
    {
        "id": "T-002",
        "text": "second ticket",
        "truth": {
            "category": "refund",
            "fields": {"order_id": "ORD-11111", "customer_name": None, "product_sku": None},
            "escalate": True,
        },
    },
]
GOOD_OUTPUT = (
    '{"category": "billing", "escalate": false, '
    '"fields": {"order_id": null, "customer_name": null, "product_sku": null}}'
)


def _agent_that_returns(outputs):
    seen = []

    def agent(text):
        seen.append(text)
        return outputs[len(seen) - 1]

    agent.seen = seen
    return agent


class RunShadowTest(unittest.TestCase):
    def test_agent_is_called_once_per_ticket_in_order(self):
        agent = _agent_that_returns([GOOD_OUTPUT, GOOD_OUTPUT])
        run_shadow(TICKETS, agent)
        self.assertEqual(agent.seen, ["first ticket", "second ticket"])

    def test_record_keeps_human_resolution_beside_raw_agent_output(self):
        agent = _agent_that_returns([GOOD_OUTPUT, "not json"])
        first, second = run_shadow(TICKETS, agent)
        self.assertEqual(first["id"], "T-001")
        self.assertEqual(first["human"], TICKETS[0]["truth"])
        self.assertEqual(first["agent_raw"], GOOD_OUTPUT)
        self.assertEqual(second["agent_raw"], "not json")

    def test_unparseable_output_is_logged_as_none_not_raised(self):
        agent = _agent_that_returns([GOOD_OUTPUT, "not json"])
        _, second = run_shadow(TICKETS, agent)
        self.assertIsNone(second["agent"])

    def test_parseable_output_is_stored_as_prediction(self):
        agent = _agent_that_returns([GOOD_OUTPUT, GOOD_OUTPUT])
        first, _ = run_shadow(TICKETS, agent)
        self.assertEqual(first["agent"]["category"], "billing")
