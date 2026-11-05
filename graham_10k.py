"""Run the shared SEC 10-K engine and print the Lab 19 Graham checks."""

import argparse
import json
import os
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parents[2] / "edgar-buffett-10k" / "scripts"
sys.path.insert(0, str(SHARED))
from edgar_buffett import build_report, compute_panel_checks  # noqa: E402
from graham_rules import CURRENT_RATIO_MINIMUM


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    parser.add_argument("--user-agent", default=os.environ.get("SEC_USER_AGENT"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = build_report(args.ticker, args.user_agent)
    report["panel_checks"] = compute_panel_checks(report["rows"], CURRENT_RATIO_MINIMUM)
    latest = report["rows"][-1]
    print(f"{report['ticker']} Graham checks | SEC 10-K facts only")
    print(f"Latest current ratio ({latest['fiscal_year_end']}): " + ("not known" if latest["current_ratio"] is None else f"{latest['current_ratio']:.2f}"))
    for label, status in report["panel_checks"]["graham"].items():
        print(f"{label}: {status}")
    if args.output:
        args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
