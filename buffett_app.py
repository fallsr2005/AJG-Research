"""Streamlit interface for the Lab 18 SEC EDGAR Buffett skill."""

import json
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
SKILL_SCRIPT = ROOT / ".agents" / "skills" / "edgar-buffett-10k" / "scripts"
OUTPUTS = ROOT / "lab18_outputs"
sys.path.insert(0, str(SKILL_SCRIPT))
from edgar_buffett import build_report, memo_unprinted_numbers, money_display, ratio_display  # noqa: E402


def cached_report(ticker: str):
    path = OUTPUTS / f"{ticker.upper()}_10k_report.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


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
                "ROE": ratio_display(row["roe"]),
                "Owner earnings": money_display(row["owner_earnings"]),
            }
        )
    return pd.DataFrame(rows)


st.set_page_config(page_title="Buffett 10-K skill", layout="wide")
st.title("Buffett 10-K skill")
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
        st.warning("Enter a name-and-email SEC contact to download a ticker that has no saved code-computed report.")
        st.stop()
    try:
        report = live_report(ticker, contact)
    except (ValueError, RuntimeError) as error:
        st.error(str(error))
        st.stop()

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

st.subheader("Buffett checks")
for label, status in report["checks"].items():
    st.write(f"**{label.replace('_', ' ')}:** {status}")

memo_path = OUTPUTS / f"{ticker}_buffett_memo.md"
st.subheader("Buffett-style memo")
if memo_path.exists():
    memo = memo_path.read_text(encoding="utf-8")
    st.markdown(memo)
    unexpected = memo_unprinted_numbers(memo, report)
    if unexpected:
        st.error("Numbers in the memo not printed by the script: " + ", ".join(unexpected))
    else:
        st.success("Every number in this memo was printed by the SEC-EDGAR script.")
else:
    st.info("No saved memo for this ticker. Use the edgar-buffett-10k skill after running the script.")
