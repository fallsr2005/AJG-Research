"""Streamlit panel for the Lab 18 Buffett, Lab 19 Graham, and Burry skills."""

import json
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
SKILL_SCRIPT = ROOT / ".agents" / "skills" / "edgar-buffett-10k" / "scripts"
GRAHAM_SCRIPT = ROOT / ".agents" / "skills" / "edgar-graham-10k" / "scripts"
OUTPUTS = ROOT / "lab18_outputs"
sys.path.insert(0, str(SKILL_SCRIPT))
sys.path.insert(0, str(GRAHAM_SCRIPT))
from edgar_buffett import build_report, memo_unprinted_numbers, money_display, ratio_display  # noqa: E402
from edgar_buffett import compute_panel_checks  # noqa: E402
from graham_rules import CURRENT_RATIO_MINIMUM  # noqa: E402

CHECK_LABELS = {
    "buffett": {
        "roe_15_or_more_every_year": "ROE of 15% or more every year",
        "owner_earnings_positive_every_year": "Owner earnings positive every year",
        "owner_earnings_grew_first_to_last": "Owner earnings grew, first year to last",
    },
    "graham": {
        "current_ratio_2_or_more_latest_year": "Current ratio of 2 or more, latest year",
        "net_income_positive_every_year": "Net income positive every year",
        "net_income_grew_first_to_last": "Net income grew, first year to last",
    },
    "burry": {
        "operating_cash_flow_at_least_net_income_every_year": "Operating cash flow at least net income every year",
        "liabilities_no_more_than_twice_equity_latest_year": "Liabilities no more than twice equity, latest year",
    },
}


def cached_report(ticker: str):
    path = OUTPUTS / f"{ticker.upper()}_10k_report.json"
    if not path.exists():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    required = {"assets_current", "liabilities_current", "current_ratio", "liabilities_to_equity"}
    return report if required.issubset(report["rows"][0]) else None


@st.cache_data(ttl=3_600, show_spinner=False)
def live_report(ticker: str, user_agent: str):
    return build_report(ticker, user_agent)


def display_rows(report):
    rows = []
    for row in report["rows"]:
        rows.append(
            {
                "Fiscal year end": row["fiscal_year_end"],
                "Revenue": money_display(row["revenue"]["value"]),
                "Revenue tag": row["revenue"]["tag"],
                "Net income": money_display(row["net_income"]["value"]),
                "Net income tag": row["net_income"]["tag"],
                "Operating cash flow": money_display(row["operating_cash_flow"]["value"]),
                "Operating cash flow tag": row["operating_cash_flow"]["tag"],
                "Capital spending": money_display(row["capital_spending"]["value"]),
                "Capital spending tag": row["capital_spending"]["tag"],
                "Equity": money_display(row["equity"]["value"]),
                "Equity tag": row["equity"]["tag"],
                "Liabilities": money_display(row["liabilities"]["value"]),
                "Liabilities tag": row["liabilities"]["tag"],
                "Current assets": money_display(row["assets_current"]["value"]),
                "Current-assets tag": row["assets_current"]["tag"],
                "Current liabilities": money_display(row["liabilities_current"]["value"]),
                "Current-liabilities tag": row["liabilities_current"]["tag"],
                "ROE": ratio_display(row["roe"]),
                "Owner earnings": money_display(row["owner_earnings"]),
                "Current ratio": "not known" if row["current_ratio"] is None else f"{row['current_ratio']:.2f}",
                "Liabilities / equity": "not known" if row["liabilities_to_equity"] is None else f"{row['liabilities_to_equity']:.2f}",
            }
        )
    return pd.DataFrame(rows)


def panel_checks(report):
    investors = {
        "buffett": report["checks"],
        "graham": report["panel_checks"]["graham"],
        "burry": report["panel_checks"]["burry"],
    }
    rows = []
    for investor, checks in investors.items():
        for check, status in checks.items():
            label = CHECK_LABELS[investor][check]
            if check == "current_ratio_2_or_more_latest_year":
                label = f"Current ratio of {CURRENT_RATIO_MINIMUM:.1f} or more, latest year"
            rows.append({"Investor": investor.title(), "Check": label, "Result": status})
    return pd.DataFrame(rows), investors


def verdict(investor: str, checks: dict[str, str]) -> str:
    if any(value == "not known" for value in checks.values()):
        return "watch it — evidence gap"
    if all(value == "pass" for value in checks.values()):
        return "own the business" if investor == "buffett" else "watch it"
    return "watch it" if investor in {"graham", "burry"} else "pass"


def show_memo(investor: str, ticker: str, report: dict, column) -> list[str]:
    path = OUTPUTS / f"{ticker}_{investor}_memo.md"
    with column:
        st.markdown(f"### {investor.title()}")
        if not path.exists():
            st.info("No saved memo yet for this skill and ticker.")
            return []
        memo = path.read_text(encoding="utf-8")
        st.markdown(memo)
        unexpected = memo_unprinted_numbers(memo, report)
        if unexpected:
            st.error("Unprinted memo numbers: " + ", ".join(unexpected))
        else:
            st.success("All memo numbers were printed by the SEC script.")
        return unexpected


st.set_page_config(page_title="Legend investor panel", layout="wide")
st.title("Legend investor panel")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    ticker = st.text_input("Ticker", value="COST").upper().strip()
    contact = st.text_input(
        "SEC contact: name and email (used only in the request header)",
        value=os.environ.get("SEC_USER_AGENT", ""),
        type="password",
    )

if not ticker:
    st.stop()

report = cached_report(ticker)
if report is None:
    if not contact:
        st.warning("Enter a name-and-email SEC contact to download a ticker with no saved Lab 19 report.")
        st.stop()
    try:
        report = live_report(ticker, contact)
    except (ValueError, RuntimeError) as error:
        st.error(str(error))
        st.stop()

# The panel always uses Graham's currently stated skill threshold, including the probe.
report["panel_checks"] = compute_panel_checks(report["rows"], CURRENT_RATIO_MINIMUM)

st.subheader(f"{report['ticker']} — {report['company_name']}")
chart_rows = []
for row in report["rows"]:
    chart_rows.append(
        {
            "Fiscal year end": row["fiscal_year_end"],
            "Owner earnings": None if row["owner_earnings"] is None else row["owner_earnings"] / 1_000_000,
            "Net income": None if row["net_income"]["value"] is None else row["net_income"]["value"] / 1_000_000,
        }
    )
st.line_chart(pd.DataFrame(chart_rows).set_index("Fiscal year end"), width="stretch")
st.caption("USD millions. Missing values remain missing; the app does not estimate them.")

st.subheader("SEC 10-K facts and calculated measures")
st.dataframe(display_rows(report), width="stretch", hide_index=True)

st.subheader("Legend investor panel")
check_table, investor_checks = panel_checks(report)
check_table["Verdict"] = check_table["Investor"].str.lower().map(
    {name: verdict(name, checks) for name, checks in investor_checks.items()}
)
st.dataframe(check_table, width="stretch", hide_index=True)

st.subheader("Three memos")
columns = st.columns(3)
flags = []
for investor, column in zip(("buffett", "graham", "burry"), columns):
    flags.extend(show_memo(investor, ticker, report, column))
if flags:
    st.error("Panel number audit found: " + ", ".join(sorted(set(flags))))
else:
    st.success("Every number across the saved panel memos was printed by the SEC-EDGAR script.")
