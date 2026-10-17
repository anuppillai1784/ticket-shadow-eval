from shadow_eval.model import CATEGORIES, FIELD_NAMES
from shadow_eval.stats import wilson_interval


def summarize(rows):
    """Aggregate scored rows into overall, per-category and escalation metrics."""
    if not rows:
        raise ValueError("cannot summarize zero tickets")
    scores = [row["score"] for row in rows]
    field_matches = sum(sum(score["fields_correct"].values()) for score in scores)
    return {
        "tickets": len(rows),
        "parse_failures": sum(score["parse_failed"] for score in scores),
        "category": _proportion(_count(scores, "category_correct"), len(scores)),
        "per_category": _per_category(rows),
        "fields": _proportion(field_matches, len(scores) * len(FIELD_NAMES)),
        "escalation": _escalation(scores),
    }


def _per_category(rows):
    per_category = {}
    for category in CATEGORIES:
        group = [row["score"] for row in rows if row["human"]["category"] == category]
        if group:
            per_category[category] = _proportion(_count(group, "category_correct"), len(group))
    return per_category


def _escalation(scores):
    flagged = [score["escalate_flagged"] for score in scores]
    expected = [score["escalate_expected"] for score in scores]
    true_positive = _pairs(flagged, expected, True, True)
    false_positive = _pairs(flagged, expected, True, False)
    false_negative = _pairs(flagged, expected, False, True)
    return {
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "true_negative": _pairs(flagged, expected, False, False),
        "precision": _ratio(true_positive, true_positive + false_positive),
        "recall": _ratio(true_positive, true_positive + false_negative),
    }


def _pairs(flagged, expected, flag_value, expected_value):
    return sum(
        1 for flag, truth in zip(flagged, expected) if flag == flag_value and truth == expected_value
    )


def _count(scores, key):
    return sum(score[key] for score in scores)


def _ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def _proportion(correct, total):
    low, high = wilson_interval(correct, total)
    return {"correct": correct, "total": total, "rate": correct / total, "low": low, "high": high}
