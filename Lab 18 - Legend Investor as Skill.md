# Lab 18 — Legend Investor as Skill

## Question and skill boundary

Can an investor's philosophy become a skill the AI runs consistently—every number computed from the 10-K, with the model limited to judgment?

The repo-scoped skill is [edgar-buffett-10k](.agents/skills/edgar-buffett-10k/SKILL.md). It is discovered from `.agents/skills`; its deterministic script downloads only SEC EDGAR's public ticker map and companyfacts data. It does not install or use FAskills, its paid services, price data, news, or estimates.

## What code computes and what judgment supplies

Code selects 10-K annual facts, keeps the latest filing for a duplicated fiscal period, chooses the specified XBRL tags, calculates ROE and owner earnings, and runs the three fixed checks. The model may only use those printed results to judge the business as **own the business**, **watch it**, or **pass**. It does not judge price this week.

The script requires a name-and-email SEC User-Agent at runtime through `SEC_USER_AGENT`; it does not write that personal contact information to a file. A missing source fact prints `not found`, and every dependent calculation/check prints `not known` rather than an estimate.

## Commands

```powershell
$env:SEC_USER_AGENT = "Your Name your.email@example.com"
python .agents/skills/edgar-buffett-10k/scripts/edgar_buffett.py COST --output lab18_outputs/COST_10k_report.json
python -m streamlit run buffett_app.py
```

## COST verification

The code-computed report and memo are saved in `lab18_outputs/`. The results below were produced by the script from the public SEC companyfacts endpoint on 2026-11-03; values are USD millions.

| FY end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2022-08-28 | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3% | 3,501 |
| 2023-09-03 | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1% | 6,745 |
| 2024-09-01 | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2% | 6,629 |
| 2025-08-31 | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8% | 7,837 |
| 2026-08-30 | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8% | 9,382 |

Every required value matches the Lab 18 known answer. The selected XBRL tags were `RevenueFromContractWithCustomerExcludingAssessedTax`, `NetIncomeLoss`, `NetCashProvidedByUsedInOperatingActivities`, `PaymentsToAcquirePropertyPlantAndEquipment`, and `StockholdersEquity`.

| Buffett check | COST result |
|---|---|
| ROE at least 15% every year | pass |
| Owner earnings positive every year | pass |
| Owner earnings grew from first to last | pass |

### Probes

- **JPM:** Capital spending printed `not found` in every displayed year because neither permitted capital-spending tag was present. Owner earnings printed `not found`; both owner-earnings checks printed `not known`. The script did not estimate any of those values.
- **Memo source check:** The saved COST memo produced no unprinted-number flags. Adding `40.0%` to that memo produced the flag `40`, proving the app is checking numerals against the script's output rather than accepting typed figures.

## Decision

**I trust the Buffett-style COST verdict for the reported five-year record because its source facts, calculations, and three checks are repeatable from SEC 10-K data; I would revisit it if a required metric became not found or a check failed.** This is a business-quality judgment based only on the five printed 10-K rows, not a recommendation or price opinion.

## Learning and reflection

An agent skill is a small discoverable folder: Codex initially sees its name and description, then reads the full `SKILL.md` only if the task matches. That progressive disclosure keeps unrelated instructions out of the working context.

The skill makes extraction, tag priority, date selection, calculations, missing-data treatment, and the three checks repeatable. It leaves the short business-quality verdict to the model. Numbers belong in code because the same stated inputs should yield the same arithmetic every run; the model should not recreate source extraction or calculation from prose. “Not found” is better than an estimate because it makes the evidence gap visible instead of silently converting uncertainty into a false fact.
