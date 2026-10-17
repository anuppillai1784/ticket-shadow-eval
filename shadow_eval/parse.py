import json


def parse_prediction(raw):
    """Return the agent prediction dict, or None when the output is malformed."""
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return value if _is_prediction(value) else None


def _is_prediction(value):
    return (
        isinstance(value, dict)
        and isinstance(value.get("category"), str)
        and isinstance(value.get("fields"), dict)
        and isinstance(value.get("escalate"), bool)
    )
