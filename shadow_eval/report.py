from shadow_eval.report_tables import table

PROPORTION_HEADERS = ["Correct", "Total", "Rate", "Wilson 95%"]
ESCALATION_HEADERS = [
    "True positive",
    "False positive",
    "False negative",
    "True negative",
    "Precision",
    "Recall",
]
FAILURE_HEADERS = [
    "Ticket",
    "Human category",
    "Agent category",
    "Wrong fields",
    "Human escalate",
    "Agent escalate",
]


def failed_rows(rows):
    return [row for row in rows if _is_failure(row["score"])]


def render_report(seed, rows, summary, gates, verdict):
    sections = [
        "# Shadow evaluation report",
        f"- Seed: {seed}\n- Tickets: {summary['tickets']}\n- Verdict: {verdict}",
        _section("Gates", _gates_table(gates)),
        _section("Overall accuracy", _overall_table(summary)),
        _section("Per category", _per_category_table(summary)),
        _section("Escalation", _escalation_table(summary)),
        _section("Failures", _failures_table(rows)),
    ]
    return "\n\n".join(sections) + "\n"


def _section(title, body):
    return f"## {title}\n\n{body}"


def _is_failure(score):
    return (
        score["parse_failed"]
        or not score["category_correct"]
        or not all(score["fields_correct"].values())
        or not score["escalate_correct"]
    )


def _rate(value):
    return "n/a" if value is None else f"{value:.3f}"


def _yes_no(flag):
    return "yes" if flag else "no"


def _proportion_cells(label, block):
    interval = f"[{_rate(block['low'])}, {_rate(block['high'])}]"
    return [label, str(block["correct"]), str(block["total"]), _rate(block["rate"]), interval]


def _gates_table(gates):
    rows = [
        [
            gate["metric"],
            _rate(gate["value"]),
            _rate(gate["required"]),
            "PASS" if gate["passed"] else "FAIL",
        ]
        for gate in gates
    ]
    return table(["Metric", "Value", "Required", "Result"], rows)


def _overall_table(summary):
    rows = [
        _proportion_cells("Category", summary["category"]),
        _proportion_cells("Field slot", summary["fields"]),
    ]
    body = table(["Measure", *PROPORTION_HEADERS], rows)
    return f"{body}\n\nUnparsed agent outputs: {summary['parse_failures']}"


def _per_category_table(summary):
    rows = [
        _proportion_cells(category, block)
        for category, block in summary["per_category"].items()
    ]
    return table(["Category", *PROPORTION_HEADERS], rows)


def _escalation_table(summary):
    escalation = summary["escalation"]
    row = [
        str(escalation["true_positive"]),
        str(escalation["false_positive"]),
        str(escalation["false_negative"]),
        str(escalation["true_negative"]),
        _rate(escalation["precision"]),
        _rate(escalation["recall"]),
    ]
    return table(ESCALATION_HEADERS, [row])


def _failures_table(rows):
    failures = failed_rows(rows)
    if not failures:
        return "No failed tickets."
    return table(FAILURE_HEADERS, [_failure_cells(row) for row in failures])


def _failure_cells(row):
    score = row["score"]
    agent = row["agent"]
    wrong = [name for name, correct in score["fields_correct"].items() if not correct]
    return [
        row["id"],
        row["human"]["category"],
        agent["category"] if agent else "unparsed",
        ", ".join(wrong) if wrong else "none",
        _yes_no(score["escalate_expected"]),
        "unparsed" if agent is None else _yes_no(score["escalate_flagged"]),
    ]
