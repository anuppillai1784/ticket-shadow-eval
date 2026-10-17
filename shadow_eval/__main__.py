import argparse
import sys

from shadow_eval.pipeline import evaluate, write_outputs
from shadow_eval.report import render_report
from shadow_eval.summary import summarize
from shadow_eval.verdict import Thresholds, check_gates, verdict_for

DEFAULT_SEED = 7
DEFAULT_OUT = "examples"


def main(argv=None):
    args = _parse_args(argv)
    thresholds = _thresholds_from(args)
    rows = evaluate(args.seed)
    summary = summarize(rows)
    gates = check_gates(summary, thresholds)
    verdict = verdict_for(gates)
    write_outputs(args.out, rows, render_report(args.seed, rows, summary, gates, verdict))
    print(f"Verdict: {verdict}")
    return 0


def _parse_args(argv):
    defaults = Thresholds()
    parser = argparse.ArgumentParser(
        prog="shadow_eval",
        description="Shadow-test a ticket agent against historical human resolutions.",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="generator seed")
    parser.add_argument("--out", default=DEFAULT_OUT, help="directory for results and report")
    parser.add_argument("--min-category-accuracy", type=float, default=defaults.category_accuracy)
    parser.add_argument("--min-field-accuracy", type=float, default=defaults.field_accuracy)
    parser.add_argument(
        "--min-escalation-precision", type=float, default=defaults.escalation_precision
    )
    parser.add_argument("--min-escalation-recall", type=float, default=defaults.escalation_recall)
    return parser.parse_args(argv)


def _thresholds_from(args):
    return Thresholds(
        category_accuracy=args.min_category_accuracy,
        field_accuracy=args.min_field_accuracy,
        escalation_precision=args.min_escalation_precision,
        escalation_recall=args.min_escalation_recall,
    )


if __name__ == "__main__":
    sys.exit(main())
