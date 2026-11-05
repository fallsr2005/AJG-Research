---
name: edgar-burry-10k
description: Screen a public-company ticker with Michael Burry's Lab 19 cash-flow and leverage checks using shared SEC EDGAR 10-K facts; do not use price, news, or estimates.
---

# SEC EDGAR Burry 10-K skill

Run `scripts/burry_10k.py TICKER` before writing a Burry memo. Set a truthful `SEC_USER_AGENT` with a name and contact email only at runtime; do not save personal contact information in the project.

The script uses the same five-year 10-K facts as the Buffett and Graham skills. It code-computes and prints:

- operating cash flow at least net income in every year;
- liabilities no more than twice year-end equity in the latest year.

Missing source facts remain `not found`; a dependent ratio or check is `not known`. Write a short, skeptical Burry-style `own the business`, `watch it`, or `pass` memo using printed values only. Do not use prices, forecasts, news, or any facts outside the shared SEC 10-K report. Save it as `lab18_outputs/<TICKER>_burry_memo.md`.
