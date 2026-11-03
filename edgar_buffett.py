"""Deterministic SEC-EDGAR 10-K facts for the Lab 18 Buffett skill."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
FLOW_TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ],
}
INSTANT_TAGS = {"equity": ["StockholdersEquity"], "liabilities": ["Liabilities"]}
DISPLAY_NAMES = {
    "revenue": "Revenue",
    "net_income": "Net income",
    "operating_cash_flow": "Operating cash flow",
    "capital_spending": "Capital spending",
    "equity": "Equity",
    "roe": "ROE",
    "owner_earnings": "Owner earnings",
}
NUMBER_PATTERN = re.compile(r"(?<![A-Za-z0-9])\$?\d[\d,]*(?:\.\d+)?%?")


def require_user_agent(user_agent: str | None) -> str:
    """Require a runtime contact without writing personal information to disk."""
    if not user_agent or "@" not in user_agent:
        raise ValueError(
            "Set SEC_USER_AGENT to your name and contact email, for example: "
            'set SEC_USER_AGENT=\"Your Name your.email@example.com\"'
        )
    return user_agent


def download_json(url: str, user_agent: str) -> dict:
    request = Request(url, headers={"User-Agent": user_agent})
    try:
        with urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"SEC EDGAR returned HTTP {error.code} for {url}.") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach SEC EDGAR: {error.reason}") from error


def ticker_to_cik(ticker: str, user_agent: str) -> tuple[int, str]:
    wanted = ticker.upper().strip()
    records = download_json(TICKERS_URL, user_agent)
    for record in records.values():
        if record["ticker"].upper() == wanted:
            return int(record["cik_str"]), record["title"]
    raise ValueError(f"{wanted}: ticker not found in SEC company_tickers.json.")


def units_for_tag(facts: dict, tag: str) -> list[dict]:
    return facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", [])


def annual_flow_entries(facts: dict, tag: str) -> list[dict]:
    """Return only 10-K facts covering one approximately annual period."""
    entries = []
    for entry in units_for_tag(facts, tag):
        if entry.get("form") != "10-K" or not entry.get("start") or not entry.get("end"):
            continue
        days = (date.fromisoformat(entry["end"]) - date.fromisoformat(entry["start"])).days
        if 330 <= days <= 380:
            entries.append(entry)
    return entries


def latest_entry(entries: list[dict]) -> dict | None:
    """Latest filing wins for a duplicated fact period."""
    if not entries:
        return None
    return max(entries, key=lambda entry: (entry.get("filed", ""), entry.get("accn", "")))


def metric_for_end(facts: dict, tags: list[str], fiscal_end: str, is_flow: bool) -> dict:
    """Select the first permitted XBRL tag that has a latest 10-K value."""
    for tag in tags:
        candidates = annual_flow_entries(facts, tag) if is_flow else [
            entry
            for entry in units_for_tag(facts, tag)
            if entry.get("form") == "10-K" and entry.get("end") == fiscal_end and not entry.get("start")
        ]
        if is_flow:
            candidates = [entry for entry in candidates if entry.get("end") == fiscal_end]
        selected = latest_entry(candidates)
        if selected is not None:
            return {"value": selected["val"], "tag": tag, "filed": selected.get("filed")}
    return {"value": None, "tag": "not found", "filed": None}


def fiscal_ends(facts: dict) -> list[str]:
    """Use annual 10-K flow end dates and select the last five fiscal years."""
    ends = set()
    for tags in FLOW_TAGS.values():
        for tag in tags:
            ends.update(entry["end"] for entry in annual_flow_entries(facts, tag))
    selected = sorted(ends)[-5:]
    if len(selected) < 5:
        raise ValueError("Fewer than five annual 10-K fiscal periods were found in companyfacts.")
    return selected


def ratio(numerator: int | float | None, denominator: int | float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def owner_earnings(operating_cash_flow: int | float | None, capex: int | float | None) -> int | float | None:
    if operating_cash_flow is None or capex is None:
        return None
    return operating_cash_flow - capex


def check_all(rows: list[dict], key: str, predicate) -> str:
    values = [row[key]["value"] if isinstance(row[key], dict) else row[key] for row in rows]
    if any(value is None for value in values):
        return "not known"
    return "pass" if all(predicate(value) for value in values) else "fail"


def compute_checks(rows: list[dict]) -> dict:
    roe_check = check_all(rows, "roe", lambda value: value >= 0.15)
    positive_check = check_all(rows, "owner_earnings", lambda value: value > 0)
    first, last = rows[0]["owner_earnings"], rows[-1]["owner_earnings"]
    if first is None or last is None:
        growth_check = "not known"
    else:
        growth_check = "pass" if last > first else "fail"
    return {
        "roe_15_or_more_every_year": roe_check,
        "owner_earnings_positive_every_year": positive_check,
        "owner_earnings_grew_first_to_last": growth_check,
    }


def printed_number_strings(report: dict) -> list[str]:
    """Numbers the memo validator may accept because this script printed them."""
    numbers = {"5", "10", "15", "15.0"}
    for row in report["rows"]:
        for part in row["fiscal_year_end"].split("-"):
            numbers.add(str(int(part)))
        for field in ("revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities"):
            value = row[field]["value"]
            if value is not None:
                numbers.add(str(round(value / 1_000_000)))
        for field in ("roe", "owner_earnings", "liabilities_to_equity"):
            value = row[field]
            if value is not None:
                numbers.add(f"{value * 100:.1f}" if field != "owner_earnings" else str(round(value / 1_000_000)))
    return sorted(numbers)


def normalized_number(token: str) -> str | None:
    """Normalize a displayed numeric token for the memo's source check."""
    cleaned = token.replace("$", "").replace(",", "").replace("%", "")
    try:
        return format(Decimal(cleaned).normalize(), "f")
    except InvalidOperation:
        return None


def memo_unprinted_numbers(memo: str, report: dict) -> list[str]:
    """Return memo numerals absent from the script's printed-number set."""
    allowed = {normalized_number(number) for number in report["printed_numbers"]}
    found = {normalized_number(token) for token in NUMBER_PATTERN.findall(memo)}
    return sorted(number for number in found if number and number not in allowed)


def build_year_row(facts: dict, fiscal_end: str) -> dict:
    """Turn one fiscal-year-end date into sourced facts and calculated measures."""
    row = {"fiscal_year_end": fiscal_end}
    for field, tags in FLOW_TAGS.items():
        row[field] = metric_for_end(facts, tags, fiscal_end, is_flow=True)
    for field, tags in INSTANT_TAGS.items():
        row[field] = metric_for_end(facts, tags, fiscal_end, is_flow=False)
    row["roe"] = ratio(row["net_income"]["value"], row["equity"]["value"])
    row["owner_earnings"] = owner_earnings(
        row["operating_cash_flow"]["value"], row["capital_spending"]["value"]
    )
    row["liabilities_to_equity"] = ratio(row["liabilities"]["value"], row["equity"]["value"])
    return row


def build_report(ticker: str, user_agent: str) -> dict:
    """Build the reproducible, code-only evidence package used by the skill and app."""
    user_agent = require_user_agent(user_agent)
    ticker = ticker.upper().strip()
    cik, company_name = ticker_to_cik(ticker, user_agent)
    facts = download_json(FACTS_URL.format(cik=cik), user_agent)
    rows = [build_year_row(facts, fiscal_end) for fiscal_end in fiscal_ends(facts)]
    report = {
        "ticker": ticker,
        "company_name": company_name,
        "cik": f"{cik:010d}",
        "source_urls": {"tickers": TICKERS_URL, "facts": FACTS_URL.format(cik=cik)},
        "units": "USD millions in display; source facts are USD",
        "rows": rows,
        "checks": compute_checks(rows),
    }
    report["printed_numbers"] = printed_number_strings(report)
    return report


def money_display(value: int | float | None) -> str:
    return "not found" if value is None else f"{value / 1_000_000:,.0f}"


def ratio_display(value: float | None) -> str:
    return "not known" if value is None else f"{value * 100:.1f}%"


def metric_display(metric: dict) -> str:
    return f"{money_display(metric['value'])} [{metric['tag']}]"


def print_report(report: dict) -> None:
    print(f"{report['ticker']} — {report['company_name']} | USD millions | SEC 10-K facts only")
    print("Fiscal end | Revenue [tag] | Net income [tag] | Operating cash flow [tag] | Capital spending [tag] | Equity [tag] | ROE | Owner earnings")
    for row in report["rows"]:
        print(
            " | ".join(
                [
                    row["fiscal_year_end"],
                    metric_display(row["revenue"]),
                    metric_display(row["net_income"]),
                    metric_display(row["operating_cash_flow"]),
                    metric_display(row["capital_spending"]),
                    metric_display(row["equity"]),
                    ratio_display(row["roe"]),
                    money_display(row["owner_earnings"]),
                ]
            )
        )
    print("\nBuffett checks")
    for label, status in report["checks"].items():
        print(f"{label}: {status}")
    print("\nA missing value is not estimated: not found; dependent ratio/check: not known.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker", help="SEC ticker, for example COST")
    parser.add_argument("--user-agent", default=os.environ.get("SEC_USER_AGENT"))
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    arguments = parser.parse_args()
    report = build_report(arguments.ticker, arguments.user_agent)
    print_report(report)
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nSaved code-computed report: {arguments.output}")


if __name__ == "__main__":
    main()
