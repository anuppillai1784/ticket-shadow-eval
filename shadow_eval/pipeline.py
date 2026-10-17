import json
import os

from shadow_eval.mock_agent import mock_agent
from shadow_eval.model import Agent
from shadow_eval.scoring import score_record
from shadow_eval.shadow import run_shadow
from shadow_eval.tickets import generate_tickets

RESULTS_FILE = "results.jsonl"
REPORT_FILE = "report.md"


def evaluate(seed, agent: Agent = mock_agent):
    """Generate tickets, run the shadow pass, and attach a score to each row."""
    records = run_shadow(generate_tickets(seed), agent)
    return [{**record, "score": score_record(record)} for record in records]


def write_outputs(out_dir, rows, report_text):
    """Write one JSON line per ticket to results.jsonl and the report to report.md."""
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, RESULTS_FILE), "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    with open(os.path.join(out_dir, REPORT_FILE), "w", encoding="utf-8") as handle:
        handle.write(report_text)
