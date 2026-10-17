# ticket-shadow-eval

## What it does

ticket-shadow-eval runs 100 synthetic support tickets through an agent. It compares each agent answer with the human resolution. It reports accuracy, the failed tickets, and a GO or NO-GO verdict.

## Why it matters

Shadow testing runs an agent beside real work before go-live. The agent output is only logged, so it cannot affect a customer.

## Quickstart

Requires Python 3.11 or newer. The project has no dependencies and no install step.

```
python3 -m unittest discover
python3 -m shadow_eval --seed 7 --out examples
```

The first command runs the tests. The second command writes `examples/results.jsonl` and `examples/report.md`. It also prints the verdict.

The command takes these options:

- `--seed N`: seed for the ticket generator. Default: 7.
- `--out DIR`: output directory. Default: `examples`.
- `--min-category-accuracy`, `--min-field-accuracy`: minimum rates for a GO. Defaults: 0.90 and 0.85.
- `--min-escalation-precision`, `--min-escalation-recall`: minimum rates for a GO. Defaults: 0.80 and 0.80.

## Repo tree

```
.gitignore                         # Paths that git must not track
LICENSE                            # MIT license
README.md                          # This guide
pyproject.toml                     # Package metadata, no dependencies
examples/report.md                 # Sample Markdown report, seed 7
examples/results.jsonl             # Sample per-ticket rows, seed 7
shadow_eval/__init__.py            # Package marker
shadow_eval/__main__.py            # Command-line entry point
shadow_eval/mock_agent.py          # Deterministic, imperfect demo agent
shadow_eval/model.py               # Categories, field names, Agent type
shadow_eval/parse.py               # Checks agent output shape
shadow_eval/pipeline.py            # Runs the evaluation and writes outputs
shadow_eval/report.py              # Builds the Markdown report
shadow_eval/report_tables.py       # Renders Markdown tables
shadow_eval/scoring.py             # Scores one ticket
shadow_eval/shadow.py              # Shadow pass: logs agent output only
shadow_eval/stats.py               # Wilson score interval
shadow_eval/summary.py             # Overall, per-category and escalation metrics
shadow_eval/templates.py           # Ticket text templates and name pools
shadow_eval/tickets.py             # Seeded synthetic ticket generator
shadow_eval/verdict.py             # Threshold gates and GO/NO-GO verdict
tests/__init__.py                  # Test package marker
tests/test_cli.py                  # CLI writes outputs and applies flags
tests/test_determinism.py          # Same seed gives identical bytes
tests/test_mock_agent.py           # Mock agent output and known misses
tests/test_parse.py                # Agent output shape checks
tests/test_report.py               # Report lists exactly the failed tickets
tests/test_scoring.py              # Per-ticket scoring rules
tests/test_shadow.py               # Shadow pass logs and never raises
tests/test_summary.py              # Aggregate metrics and edge cases
tests/test_tickets.py              # Ticket generator behavior
tests/test_verdict.py              # GO/NO-GO gate behavior
tests/test_wilson.py               # Wilson interval known values
```

## How it works

The generator makes 100 tickets from one seed. Each category gets 20 tickets. Each ticket has messy text, a human resolution, and three fields. The fields are order ID, customer name, and product code. A field can be missing. The text can contain typos, a second issue, and an escalation line.

The agent is any function that takes text and returns a string. The string must be a JSON object with the keys `category`, `fields`, and `escalate`. The built-in `mock_agent` uses keyword rules. Its rules miss some cases on purpose.

The shadow pass calls the agent on each ticket. It writes the raw output beside the human resolution. No code reads the prediction to take an action. Output that is not valid JSON is logged as unparsed. An unparsed output counts as wrong on every item.

Scoring works as follows. A category is correct when it matches after trimming and lowercasing. Each of the three field slots counts. A missing human value matches only a missing answer. Escalation uses the flag from the agent. Precision and recall use the human escalate flag. A ratio with a zero denominator shows as n/a and fails its gate.

The report gives a Wilson 95% interval for each accuracy rate. The Wilson interval is a 95% range for the true rate. Small samples give wide ranges. A gate passes when its value is at or above its threshold. One failed gate gives NO-GO.

The same seed always gives the same bytes in both output files. The outputs have no timestamps or run IDs.

## Sample output

The quickstart run with seed 7 writes this summary. The full report is in `examples/report.md`.

```
- Seed: 7
- Tickets: 100
- Verdict: NO-GO

| Metric | Value | Required | Result |
|---|---|---|---|
| category_accuracy | 0.640 | 0.900 | FAIL |
| field_accuracy | 0.900 | 0.850 | PASS |
| escalation_precision | 0.692 | 0.800 | FAIL |
| escalation_recall | 0.643 | 0.800 | FAIL |

| Measure | Correct | Total | Rate | Wilson 95% |
|---|---|---|---|---|
| Category | 64 | 100 | 0.640 | [0.542, 0.727] |
| Field slot | 270 | 300 | 0.900 | [0.861, 0.929] |
```

## Limits

- All names, order IDs, and product codes are synthetic. The demo data has no prices.
- The mock agent is a demo. Its accuracy says nothing about a real agent.
- The default thresholds are example policy values. Set your own with the flags.
- Gates compare the point estimate with the threshold. They do not use the Wilson lower bound.
- This tool does not connect to a live ticket system. It cannot prove that a live agent is safe.
- The process exits with code 0 for GO and for NO-GO. Read the verdict line or the report.
