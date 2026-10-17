from dataclasses import dataclass

GO = "GO"
NO_GO = "NO-GO"


@dataclass(frozen=True)
class Thresholds:
    category_accuracy: float = 0.90
    field_accuracy: float = 0.85
    escalation_precision: float = 0.80
    escalation_recall: float = 0.80


def check_gates(summary, thresholds):
    """Compare each summary metric with its threshold. An undefined metric fails."""
    values = {
        "category_accuracy": summary["category"]["rate"],
        "field_accuracy": summary["fields"]["rate"],
        "escalation_precision": summary["escalation"]["precision"],
        "escalation_recall": summary["escalation"]["recall"],
    }
    return [
        _gate(metric, value, getattr(thresholds, metric)) for metric, value in values.items()
    ]


def verdict_for(gates):
    return GO if all(gate["passed"] for gate in gates) else NO_GO


def _gate(metric, value, required):
    return {
        "metric": metric,
        "value": value,
        "required": required,
        "passed": value is not None and value >= required,
    }
