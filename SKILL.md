---
name: edgar-buffett-10k
description: Analyze a public-company ticker with Buffett-style business checks using only the last five SEC EDGAR 10-K facts. Use when asked for owner earnings, ROE, or a short Buffett-style business verdict; do not use price data or non-SEC data.
---

# SEC EDGAR Buffett 10-K skill

Run `scripts/edgar_buffett.py TICKER` before writing a memo. Supply a truthful SEC-compliant User-Agent at runtime with `SEC_USER_AGENT` (name plus contact email); never save that contact information in this skill or project files.

The script is the source of every number. It downloads the SEC ticker-to-CIK map and `companyfacts` data, uses only 10-K annual facts, and returns the five latest fiscal-year-end rows. It applies these rules:

- use the latest filed 10-K when the same fiscal period appears in multiple filings;
- use `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues`;
- use `NetIncomeLoss`, `NetCashProvidedByUsedInOperatingActivities`, `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets`, and `StockholdersEquity`;
- calculate ROE as net income divided by year-end equity and owner earnings as operating cash flow minus capital spending;
- print `not found` rather than estimating a missing value; return `not known` for a ratio or check with a missing input, or with zero/negative equity.

For a memo, use only values and check results the script printed. Make a short business-only judgment: `own the business`, `watch it`, or `pass`. Do not use price, intrinsic value, targets, forecasts, or external facts. Save the memo in `lab18_outputs/<TICKER>_buffett_memo.md` and run the Streamlit app to flag any numeral that was not printed by the script.

Run the app with `python -m streamlit run buffett_app.py`.
