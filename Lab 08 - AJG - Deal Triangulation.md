# Lab 08 - AJG - Deal Evidence and Valuation Triangulation

## Scope and comparison date

**Target:** Arthur J. Gallagher & Co. (NYSE: AJG)  
**Comparison date:** September 3, 2026  
**Question:** What would AJG's share be worth at defensible peer P/E multiples, and how does that compare with the FCFF DCF?

September 3, 2026 is the valuation date used in the existing AJG research report. All three share prices below are USD Nasdaq `Close/Last` values on that same trading date. The exact returned rows and retrieval method are preserved in the [saved Nasdaq price record](</C:/Users/rocco/OneDrive/Documents/FIN_43900/Lab 08 - AJG - Nasdaq Price Evidence.md>). Annual earnings use FY2025 total reported GAAP diluted EPS, not adjusted EPS, and were public before the comparison date.

## Reopen and explain

I reran the saved DCF with `python dcf.py`. Before using AJG inputs, I ran `python comparable_policy.py --verify-lab07`; the saved Asbury regression check passed, reproducing the $215.81 to $246.18 range, $231.00 median-implied price, and -$15.18 result when Group 1 was removed. I then ran the calculator with the AJG inputs documented below.

Working explanation of the method: a peer's P/E is its price per share divided by annual diluted EPS. Multiplying that peer P/E by AJG's annual diluted EPS gives a peer-implied AJG share price. This is an equity-value comparison, so it does not use the FCFF DCF's separate enterprise-to-equity cash/debt bridge.

AJG earns primarily from insurance-brokerage commissions and fees, with related reinsurance brokerage, consulting, and third-party claims administration. Brokerage accounted for 87% of 2025 revenue and risk management accounted for 13%. [AJG 2025 Form 10-K, Item 1](https://www.sec.gov/Archives/edgar/data/354190/000162828026008662/ajg-20251231.htm)

## Define/Discover: peer policy before names

**Initial peer policy.** Consider only publicly traded, U.S.-listed insurance-brokerage and risk-advisory firms that:

- earn material recurring commission, fee, or brokerage revenue from commercial-risk, reinsurance, or employee-benefits advisory services;
- report positive annual GAAP diluted EPS in a compatible USD per-share basis that was public by September 3, 2026; and
- have a same-date closing price that can be sourced.

Qualify rather than hide material differences in consulting mix, geography, acquisition activity, unusual gains/losses, or financing. Reject an insurer that mainly bears underwriting risk, a pure claims administrator without a comparable brokerage business, a company with negative/unverifiable annual GAAP EPS, or a company without an observable same-date price.

The main research need is whether the peers' reported GAAP EPS is comparable to AJG's after its 2025 acquisitions and related integration/amortization effects. A lower peer P/E is not automatically a better value; it may reflect different growth, risk, business mix, or accounting effects.

**Two independent AI candidate-screen records:** I supplied two separate AI screens with AJG, the September 3, 2026 comparison date, and this fixed policy. The prompt requested no more than two operating-company candidates, primary-source business-model support, a material difference, and annual reported diluted EPS public by the comparison date; it did not ask either screen to rank a candidate or change the policy.

| Screen | Candidate leads returned | Independent-screen result used here |
|---|---|---|
| 1 | AON and MRSH | Identified Aon's Risk Capital brokerage/reinsurance activities and its Human Capital and NFP Wealth-gain qualifications; identified Marsh Risk/Guy Carpenter activities and Marsh's consulting-mix qualification. |
| 2 | AON and MRSH | Independently identified the same two companies and the same core qualifications, including reported GAAP EPS rather than adjusted EPS. |

The suggestions were leads only. The use-with-qualification decisions, dates, prices, and calculations below were made after checking the cited company sources and same-date-price evidence.

## Represent: two sourced candidates and decisions

| Candidate | Decision | Business-model evidence | Important qualification |
|---|---|---|---|
| Aon plc (AON) | Use with qualification | Aon describes itself as a global professional-services firm with Risk Capital and Human Capital capabilities. Its Risk Capital business includes commercial-risk insurance/specialty brokerage, global risk consulting, captives management, reinsurance, and capital markets. [Aon 2025 Form 10-K, Item 1 and Note 17](https://www.sec.gov/Archives/edgar/data/315293/000162828026008116/aon-20251231.htm) | Aon has a much broader Human Capital business. Its 2025 GAAP income also included a $1.2 billion gain from the disposal of NFP Wealth, so its reported EPS may not be fully comparable to AJG's acquisition-affected GAAP EPS. |
| Marsh (MRSH; formerly Marsh McLennan/NYSE: MMC) | Use with qualification | Marsh's Risk and Insurance Services segment includes Marsh Risk insurance broking/risk advisory and Guy Carpenter reinsurance. [Marsh 2025 Form 10-K, Risk and Insurance Services](https://www.sec.gov/Archives/edgar/data/62709/000006270926000022/mrsh-20251231.htm) | Consulting represented 36% of 2025 revenue, creating a material mix difference from AJG's brokerage-heavy model. Its 2025 results also reflected the McGriff acquisition and debt-funded interest expense. |

Both candidates meet the stated core-business policy, but neither is a replica of AJG. I retained the qualifications instead of excluding either company after seeing the implied prices.

## Source table and inputs

| Company / role | Same-date closing price | FY2025 reported GAAP diluted EPS | Fiscal year end | Annual EPS first public / filing date | Source locator |
|---|---:|---:|---|---|---|
| AJG, target | $266.66 | $5.74 | Dec. 31, 2025 | Jan. 29, 2026 / Feb. 17, 2026 | [Saved Nasdaq price record](</C:/Users/rocco/OneDrive/Documents/FIN_43900/Lab 08 - AJG - Nasdaq Price Evidence.md>); [AJG FY2025 release](https://investor.ajg.com/news/news-details/2026/Arthur-J--Gallagher--Co--Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx); [10-K, Note 8, p. 96](https://www.sec.gov/Archives/edgar/data/354190/000162828026008662/ajg-20251231.htm) |
| AON, qualified peer | $327.00 | $17.02 | Dec. 31, 2025 | Jan. 30, 2026 / Feb. 13, 2026 | [Saved Nasdaq price record](</C:/Users/rocco/OneDrive/Documents/FIN_43900/Lab 08 - AJG - Nasdaq Price Evidence.md>); [Aon FY2025 release](https://aon.mediaroom.com/2026-01-30-Aon-Reports-Fourth-Quarter-and-Full-Year-2025-Results); [10-K filing index](https://www.sec.gov/Archives/edgar/data/315293/000162828026008116/0001628280-26-008116-index.htm) |
| MRSH, qualified peer | $188.46 | $8.43 | Dec. 31, 2025 | Jan. 29, 2026 / Feb. 9, 2026 | [Saved Nasdaq price record](</C:/Users/rocco/OneDrive/Documents/FIN_43900/Lab 08 - AJG - Nasdaq Price Evidence.md>); [FY2025 release](https://www.sec.gov/Archives/edgar/data/62709/000006270926000014/mmc4q2025ex991newsrelease.htm); [10-K filing index](https://www.sec.gov/Archives/edgar/data/62709/000006270926000022/0000062709-26-000022-index.htm) |

Marsh changed its NYSE symbol from `MMC` to `MRSH` effective January 14, 2026; the price source therefore uses `MRSH`, while the FY2025 filing remains traceable to Marsh McLennan. [Company symbol-change notice](https://www.marsh.com/en/corp/about/news/marsh-mclennan-to-change-nyse-symbol-to-mrsh.html)

The input bases match: all prices and EPS are USD per common share, prices are from the same trading date, and EPS is annual reported GAAP diluted EPS. I did not use AJG's $10.69 adjusted EPS, Aon's $17.07 adjusted EPS, or Marsh's $9.75 adjusted EPS because that would mix reported and non-GAAP measures.

## Implement: calculator result

The reusable standard-library calculator is [comparable_policy.py](</C:/Users/rocco/OneDrive/Documents/FIN_43900/comparable_policy.py>). It keeps the target and peer inputs editable, deduplicates peers, excludes the target, identifies missing/nonpositive inputs as not meaningful, and produces leave-one-out results without a cash/debt bridge.

```text
python comparable_policy.py
```

| Check | Calculation | Result |
|---|---|---:|
| AJG observed P/E (comparison only) | $266.66 / $5.74 | 46.456446x |
| AON P/E | $327.00 / $17.02 | 19.212691x |
| MRSH P/E | $188.46 / $8.43 | 22.355872x |
| Peer median P/E | median of AON and MRSH P/E | 20.784281x |
| AJG price at AON P/E | 19.2126909518 x $5.74 | $110.28 |
| AJG price at MRSH P/E | 22.3558718861 x $5.74 | $128.32 |
| AJG peer-implied range | low to high peer-implied price | $110.28 to $128.32 |
| AJG at peer median | 20.7842814190 x $5.74 | $119.30 |

P/E already produces an equity value per share. I did not add cash or subtract debt from the P/E-implied prices.

## Validate: manual check and changed-peer result

**Manual arithmetic check:** AON P/E = $327.00 / $17.02 = **19.212691x**, matching the calculator before display rounding.

**Prediction:** MRSH has the higher P/E, so removing MRSH should reduce AJG's median-implied value.

| Peer removed | Remaining reference estimate | Change from full-peer median |
|---|---:|---:|
| AON | $128.32 | +$9.02 |
| MRSH | $110.28 | -$9.02 |

The prediction is confirmed: removing MRSH leaves the lower AON multiple and lowers the estimate by $9.02. With one peer remaining, the result is a reference estimate rather than a range because there is no longer a low-to-high set of peer multiples. Neither peer was removed to improve the answer.

## Evolve: compare with the DCF

The current FY2025-input DCF is reproducible with:

```text
python dcf.py
```

I added the documented 9%/10%/11% WACC and 2%/3%/4% terminal-growth cases to the saved DCF so the comparison uses a current, reproducible sensitivity rather than the older training grid in `Reverse DCF - AJG.md`. This is a FY2025-input valuation model compared with the September 3, 2026 market price; it is not represented as a DCF built from September 2026 financial statements.

**DCF bridge convention:** The model uses $1,155 million of 2025 non-restricted cash rather than $1,396 million of total cash because the 10-K separately identifies $241 million of restricted cash. It uses $12,744 million of balance-sheet corporate-related borrowings ($640 million current plus $12,104 million noncurrent), rather than the earlier Lab 04 presentation of $13,099 million gross corporate-and-other debt. The latter is a different gross Note 7 measure that includes the premium-financing facility; the current DCF keeps one stated carrying-amount convention throughout. [AJG 2025 Form 10-K, cash reconciliation and Note 7](https://www.sec.gov/Archives/edgar/data/354190/000162828026008662/ajg-20251231.htm)

| Method | AJG result and comparison date | Main assumption or limitation |
|---|---|---|
| FCFF DCF | FY2025-input DCF: $67.99 to $145.58 per diluted share; $95.80 base case at 10% WACC and 3% terminal growth, compared with the Sept. 3, 2026 market price | Forecast FCFF growth, WACC, terminal growth, and the enterprise-to-equity bridge drive the result. The sensitivity cases are scenarios, not a confidence interval. |
| Peer P/E | $110.28 to $128.32; $119.30 median-implied value; prices dated Sept. 3, 2026 | Peer selection and annual reported GAAP EPS drive the result. AJG's acquisition/integration effects, Aon's disposal gain, and Marsh's consulting mix limit direct comparability. |

Both methods sit below the September 3 observed AJG close of $266.66, but I do **not** average them. The disagreement is a reason to investigate the DCF assumptions, peer policy, and earnings definitions.

### Skeptical review and judgment

**Skeptical colleague's criticism:** The weakest supported assumption is that FY2025 reported GAAP EPS transfers cleanly across these three companies. AJG's GAAP EPS is affected by large 2025 acquisitions and related integration/amortization items, while Aon's GAAP income includes a disposal gain and Marsh has a large consulting segment. These differences could make the P/E range a poor proxy for AJG's sustainable earnings power.

**Judgment: Accept.** The criticism is supported by the filings, so I retain the stated GAAP convention and peer qualifications but treat the range as a conditional reference, not a fair-value conclusion. I do not change to adjusted EPS just because it would change the result.

**Decision-changing question:** After enough post-acquisition reporting is available, do consistently defined reported GAAP EPS and cash generation show that AJG's lower FY2025 EPS was temporary, and does the peer-multiple gap persist after accounting for Aon's disposal gain and Marsh's consulting mix?

**Answer:** The present sources do not resolve that question. I would need subsequent annual reporting that separates sustainable brokerage earnings, integration/amortization effects, cash generation, and deleveraging, plus a refreshed peer comparison on the same earnings definition.

## Reflect: conditional conclusion

**Call: Watch-defer.** AJG has a credible brokerage and risk-management business, and both selected peers share important insurance-brokerage economics. However, the peer range and the current DCF sensitivity are materially below the observed market price, while the FY2025 GAAP earnings bases have meaningful acquisition, disposal, and business-mix qualifications. The evidence does not support an initiate call at this time, but the earnings-comparability limits also make a definitive do-not-initiate call premature.

I would reconsider toward initiate if later filings show durable post-acquisition reported earnings and cash generation, lower leverage, and a source-supported peer comparison that remains favorable on a consistent EPS basis. I would reconsider toward do-not-initiate if those filings show that integration costs, leverage, or acquisitions continue to prevent the expected earnings conversion.

## Course source

[Lab 08: Deal Evidence and Valuation Triangulation](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-08-deal-triangulation.md)

## GitHub checkout status

This folder has no Git repository, remote, branch, or student-owned GitHub destination. I therefore cannot provide truthful GitHub links for these local submission files yet. After the files are committed and pushed to the student's actual repository, add the live blob links for:

- [Lab 08 report](</C:/Users/rocco/OneDrive/Documents/FIN_43900/Lab 08 - AJG - Deal Triangulation.md>)
- [Comparable-company calculator](</C:/Users/rocco/OneDrive/Documents/FIN_43900/comparable_policy.py>)
- [DCF calculator](</C:/Users/rocco/OneDrive/Documents/FIN_43900/dcf.py>)
- [Saved price evidence](</C:/Users/rocco/OneDrive/Documents/FIN_43900/Lab 08 - AJG - Nasdaq Price Evidence.md>)

*Educational analysis only; not investment advice.*
