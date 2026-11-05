# Lab 19 — Legend Panel

## Question

When Buffett, Graham, and Burry read the same SEC 10-K facts, where do they agree, where do they split, and should the panel screen Project 2 companies?

## Panel design

The three repo-scoped skills use the same five annual SEC EDGAR 10-K facts. The shared engine selects the specified XBRL tags, uses the latest filing for a duplicated period, and keeps a missing source value as `not found`. A dependent ratio or check is `not known`; nothing is estimated.

- Buffett: ROE at least 15% every year; owner earnings positive every year; owner earnings grew.
- Graham: current ratio (`AssetsCurrent ÷ LiabilitiesCurrent`) at least 2.0 in the latest year; net income positive every year; net income grew.
- Burry: operating cash flow at least net income every year; liabilities no more than twice equity in the latest year.

The app audits all three memo files and flags any numeral it cannot trace to the SEC script output.

## Commands

```powershell
$env:SEC_USER_AGENT = "Your Name your.email@example.com"
python .agents/skills/edgar-buffett-10k/scripts/edgar_buffett.py COST --output lab18_outputs/COST_10k_report.json
python .agents/skills/edgar-graham-10k/scripts/graham_10k.py COST
python .agents/skills/edgar-burry-10k/scripts/burry_10k.py COST
python -m streamlit run buffett_app.py
```

## COST known-answer verification

| Fiscal year end | Current ratio | Liabilities ÷ equity |
|---|---:|---:|
| 2022-08-28 | 1.02 | 2.11 |
| 2023-09-03 | 1.07 | 1.75 |
| 2024-09-01 | 0.97 | 1.96 |
| 2025-08-31 | 1.03 | 1.64 |
| 2026-08-30 | 1.06 | 1.49 |

| Investor | Check | COST result |
|---|---|---|
| Buffett | ROE at least 15% every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first to last | pass |
| Graham | Current ratio at least 2.0, latest year | fail (1.06) |
| Graham | Net income positive every year | pass |
| Graham | Net income grew, first to last | pass |
| Burry | Operating cash flow at least net income every year | pass |
| Burry | Liabilities no more than twice equity, latest year | pass (1.49) |

This is Buffett 3 of 3, Graham 2 of 3, and Burry 2 of 2, matching the training answer. All COST memo numbers pass the app's source audit.

### Threshold probe

Changing `CURRENT_RATIO_MINIMUM` in `.agents/skills/edgar-graham-10k/scripts/graham_rules.py` from `2.0` to `1.0` changes COST's Graham current-ratio check from **fail** to **pass**. I keep **2.0** because it is the stated pre-set Graham screen; lowering it after seeing COST's 1.06 would create a company-specific exception.

## Project 2 company — NVDA

NVDA is NVIDIA Corporation, the largest company held by ACWI, the global-equity fund in my Project 2 universe. Its computed report and three saved memos are in `lab18_outputs/`.

| Investor | NVDA panel result | Verdict |
|---|---|---|
| Buffett | all three checks pass | own the business |
| Graham | all three checks pass; latest current ratio 3.91 | own the business |
| Burry | liabilities ÷ equity passes at 0.31; operating cash flow did not reach net income every year | watch it |

The panel agrees that NVDA's reported five-year profitability and balance-sheet screens are strong. It splits because Burry's cash-versus-income screen fails: in FY2026 operating cash flow was 102,718 million and net income was 120,067 million. The app keeps this failure visible rather than explaining it away.

## Decision

**Only with a condition:** I would let this panel screen companies for Project 2, but never make the final decision. For NVDA, I would require a follow-up review of the years where operating cash flow was below net income; I would not treat the two bullish screen results as enough to override Burry's failed check.

## Learning and reflection

Three personas can disagree while reading the same facts because they set different rules for what matters: Buffett emphasizes durable returns and owner earnings, Graham sets a conservative liquidity threshold, and Burry tests whether earnings are supported by cash. The threshold probe shows that every screen includes a design choice: moving Graham's limit from 2.0 to 1.0 changes COST's label without changing COST's facts.

The panel agreed on NVDA's profitability and leverage but split on cash conversion. A `not found` or `not known` result remains an evidence gap, not permission to estimate a favorable value.
