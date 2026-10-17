from shadow_eval.model import FIELD_NAMES


def score_record(record):
    """Compare one agent prediction with the human resolution.

    A malformed agent output (agent is None) is wrong on every item and
    counts as "not flagged" for escalation.
    """
    truth = record["human"]
    agent = record["agent"]
    parsed = agent is not None
    flagged = parsed and agent["escalate"]
    return {
        "parse_failed": not parsed,
        "category_correct": parsed and _same(agent["category"], truth["category"]),
        "fields_correct": {
            name: parsed and _same(agent["fields"].get(name), truth["fields"][name])
            for name in FIELD_NAMES
        },
        "escalate_flagged": flagged,
        "escalate_expected": truth["escalate"],
        "escalate_correct": flagged == truth["escalate"],
    }


def _same(agent_value, truth_value):
    return _normalize(agent_value) == _normalize(truth_value)


def _normalize(value):
    return None if value is None else str(value).strip().lower()
