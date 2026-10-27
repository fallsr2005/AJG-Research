# Lab 16 — Provenance Gate

## Decision question

On the day a decision would have been made, what did the data actually say, and how much of the current-looking series arrived later?

`asof.py` uses the course's fictional card-spend table and a decision date of 2026-03-31. It uses only the Python standard library. Run it with:

```powershell
python asof.py
```

## Rules and known-answer verification

The program applies the following rules in the specified order: quarantine a missing ticker, remove exact duplicates, remove publications later than the decision date, and retain the latest publication available on that date for each ticker-month pair.

| Funnel step | Rows removed |
|---|---|
| Quarantined: no ticker | 11 |
| Exact duplicate | 7 |
| Published after 2026-03-31 | 3, 8, 10 |
| Older vintage replaced by a revision | 2 |
| As-of panel | 1, 4, 5, 6, 9, 12 |

| Ticker | As-of signal | Naive signal |
|---|---:|---:|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

The naive comparison removes unusable and exact-duplicate rows, but intentionally does **not** apply the decision-date cutoff. It therefore shows a later-vintage series, not information that could have been used on 31 March.

## Explain the revision rule

`keep_latest_vintage` groups each remaining record by its ticker and measured month. Within every group, it saves the record with the latest `published` date, then retains only those saved records. It runs after the decision-date filter, so “latest” means latest *available by the decision date*.

For AAA February, row 2 was published 10 March at 104.0 and row 4 was published 25 March at 103.0. Both were knowable by 31 March, so row 4 replaces row 2. The tradeable February signal is therefore `(103 / 101 - 1) × 100 = +1.98%`, rather than +2.97% from the superseded vintage.

## Point-in-time learning and reflection

Look-ahead bias occurs when an analysis lets a past decision use information released only after that decision. Event time is the month an index describes; publication time is when that number became available. A revision can change a previously measured month later, so both times matter.

For AAA, the naive +5.83% March signal uses the 10 April publication of March's 109.0 index. On 31 March, that publication did not yet exist; the latest usable value was February's revised 103.0. A backtest built on the naive column would claim it acted on a stronger March signal than anyone could have known, overstating the strategy's apparent information and potentially its performance.

The rule with the largest decision impact is the publication-date cutoff: it removes the March rows that create the seemingly stronger AAA signal. The revision rule also matters because it replaces AAA's original February value of 104.0 with the 25 March revision of 103.0.

## In-class checks to complete

- Explain the difference between the month measured and the publication date to a partner.
- Explain `keep_latest_vintage` line by line, then answer a partner question from the code.
- In a temporary copy, set `DECISION_DATE` to `2026-04-15`; the as-of signals should equal the naive signals ticker for ticker. Restore `2026-03-31` afterward.
- Complete the partner swap, discussion, and course checkout.
