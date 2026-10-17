from shadow_eval.mock_agent import mock_agent
from shadow_eval.scoring import score_record
from shadow_eval.shadow import run_shadow
from shadow_eval.tickets import generate_tickets


def evaluate(seed, agent=mock_agent):
    """Generate tickets, run the shadow pass, and attach a score to each row."""
    records = run_shadow(generate_tickets(seed), agent)
    return [{**record, "score": score_record(record)} for record in records]
