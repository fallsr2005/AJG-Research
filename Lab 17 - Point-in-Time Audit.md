# Lab 17 — Point-in-Time Audit

## Decision question

Was each number in the selected series knowable on the day it would have informed a Project 2 decision, and may Project 2 use it?

Run the application with:

```powershell
python -m streamlit run asof_app.py
```

`asof_app.py` downloads the current FRED CSV and a separate ALFRED vintage CSV for every selected series. It omits `.` missing values; it never substitutes today's data for an earlier vintage. The audit table then separates observations that arrived after the selected date from values on the same dates that have since been revised.

## Required training checks

Use an **as known on** date of 2026-10-05. The application should show the following latest values in its as-of column:

| Series | Last date known | Value |
|---|---|---:|
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | 2026-10-02 | 5.28 |
| MORTGAGE30US | 2026-10-01 | 7.28 |

For the revision probe, enter `PAYEMS` in **Add another FRED series ID** and set **as known on** to 2025-01-15. The app should show December 2024 at **159,536** in the as-of column, while today’s December 2024 value is lower and the revised-same-date count is above zero. That gap proves the table uses ALFRED rather than today’s FRED values twice.

## Project 2 data card — DGS10

**Source and link:** Federal Reserve Bank of St. Louis, [DGS10](https://fred.stlouisfed.org/series/DGS10), downloaded in the application on the date displayed under its title.

**Measure and units:** The 10-year Treasury constant-maturity rate, observed daily, in percent and not seasonally adjusted. It is relevant to the SCHR government-bond sleeve: changes in market Treasury yields affect the prices and expected risk of intermediate-term Treasury holdings.

**Publication lag:** Daily observations are typically available on the following business day. The app makes the exact lag visible: on the 2026-09-30 decision date, its last DGS10 observation was 2026-09-29 at 5.26%, a one-business-day lag. Weekends and market holidays can create several calendar days between the last observation and the decision date.

**Revisions:** This is a market-rate series expected to have little or no revision activity relative to monthly macroeconomic series; the app's revised-same-date count is the evidence used for the selected vintage, not an assumption. A nonzero count would require treating the series as revised.

**Three values checked against the source:** On 2026-10-29, the final three numeric observations downloaded from the linked FRED DGS10 CSV were checked against the FRED series data: 2026-10-23 at 5.00, 2026-10-26 at 5.00, and 2026-10-27 at 4.99. A missing day is not treated as a zero or an observation.

| Date checked | DGS10 value in app | Same value on FRED source |
|---|---:|---|
| 2026-10-23 | 5.00 | Yes |
| 2026-10-26 | 5.00 | Yes |
| 2026-10-27 | 4.99 | Yes |

## Point-in-time explanation and provisional call

A data card is a compact record of a series' source, definition, units, timing, revisions, and download date. These fields stop a leak before it starts: source and definition prevent a wrong-variable substitution; units prevent scale errors; publication timing and vintage prevent look-ahead; revisions identify whether a later download rewrote history. “Cleaned the data” is not a data card because it does not identify what the observation means, when it became knowable, or how another person can reproduce it.

A backtest using today's DGS10 history could overstate what was knowable if it includes an observation before its publication date or uses a revised historical value. The selected **as known on** date makes this visible: values absent from the ALFRED vintage were unavailable, regardless of whether FRED displays them today.

**Provisional call:** Admit DGS10 for the Project 2 audit only when each decision uses the ALFRED vintage available on that decision date. Its daily frequency and usually low revision count make it suitable for the timing audit, but it is not automatically a return forecast or a portfolio input. Reconsider this call if the app shows material revisions or if the strategy cannot apply the required publication-date delay.

## Partner attack and response

**Partner's concern:** Publication date.

**Response with evidence:** I trust the publication date because the app's ALFRED vintage dated September 30 showed DGS10 only through September 29 at 5.26%. That one-business-day gap demonstrates why Project 2 must use the value available as of each decision date.

## In-class completion checklist

- Explain why DGS10 moves the Treasury-bond sleeve to a partner.
- Verify the four 2026-10-05 values and the PAYEMS revision probe in the running app.
- Read and manually confirm three DGS10 values against FRED, then fill the data-card table above.
- Explain `download_as_known_on` line by line to a partner; answer one partner question from the code; complete the swap.
- Partner attack completed: the publication-date concern and app-based response are recorded above.
- Publish `asof_app.py` and this Markdown file to GitHub, then submit their links individually.
