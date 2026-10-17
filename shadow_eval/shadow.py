from shadow_eval.model import Agent
from shadow_eval.parse import parse_prediction


def run_shadow(tickets, agent: Agent):
    """Call the agent on each ticket and log its output. Nothing is acted on."""
    return [_shadow_record(ticket, agent(ticket["text"])) for ticket in tickets]


def _shadow_record(ticket, raw):
    return {
        "id": ticket["id"],
        "text": ticket["text"],
        "human": ticket["truth"],
        "agent_raw": raw,
        "agent": parse_prediction(raw),
    }
