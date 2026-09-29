# Lab 11 - AJG Sensitivity Analysis

## D - Question

**Which assumptions drive Arthur J. Gallagher & Co.'s (AJG) forecast and value, and what explains their effects?**

All amounts below are **USD millions**, except percentages. The model forecasts
FY2026E-FY2030E. Its final-year cash-flow output is **FCFE before dividends**.

## R - Inputs, ranges, and locked changed-input record

The two tested inputs are independent assumptions already in `ajg_proforma.py`.
Neither is a calculated statement total. Each sensitivity run changes exactly
one of them and lets the linked statements, working capital, cash, and checks
recalculate.

| Driver | Lower | Base | Higher | Affected years | Units and range reason |
|---|---|---|---|---|---|
| Organic revenue growth | 5%, 4%, 3%, 2%, 2% | 6%, 5%, 4%, 3%, 3% | 7%, 6%, 5%, 4%, 4% | FY2026E-FY2030E | Percentage of prior-year revenue; a labelled judgment of a **minus/plus 1.0 percentage-point** shift to each base-year assumption. The base begins at AJG's disclosed FY2025 organic base commission-and-fee growth of 6% and fades. The same point shift makes the range reproducible. |
| Compensation / revenue before reimbursements | 55.9% in every forecast year | 56.9% in every forecast year | 57.9% in every forecast year | FY2026E-FY2030E | Percentage of revenue; base is FY2025 compensation of $7,842m / $13,778m. The minus/plus 1.0 percentage-point range is a labelled planning judgment for operating-cost efficiency versus pressure, not a claim about probability. |

### Locked Changed-Input Record

**Locked at 2026-09-29 14:07:51 -04:00, before the official saved sensitivity run.**

| Item | Record |
|---|---|
| Changed independent input | Organic revenue-growth path: 6%, 5%, 4%, 3%, 3% to 7%, 6%, 5%, 4%, 4% (a +1.0 percentage-point shift in each FY2026E-FY2030E assumption). |
| Other independent inputs | Held at base, including compensation / revenue at 56.9%. |
| Prediction | FY2030 operating profit and FCFE before dividends will increase. I expected roughly **$150m-$250m** more operating profit and **$100m-$200m** more FCFE. |
| Why | Higher revenue flows through at fixed compensation and operating-expense ratios. Receivables and other operating balances also rise, partly offsetting the cash-flow gain. |
| Actual result | FY2030 operating profit increased **$221.0m** and FCFE before dividends increased **$161.6m**. The direction and rough size matched the prediction. |
| Prediction error / learning | There was no directional error. The FCFE gain is smaller than the EBIT gain because linked working-capital investment rises with revenue; taxes also rise with pretax income. |

## I and V - Visible output and checks

The base was run before the cases. A fresh, independent execution of the full
linked model was used for each lower/base/higher case; the runner changes the
two input lines in memory only and does not save altered base assumptions.
The official saved run completed at **2026-09-29 18:09:09 UTC**.

### Revenue-growth sensitivity

| Case | Actual revenue-growth input (FY2026E to FY2030E) | FY2030 operating profit | Change from base | FY2030 FCFE before dividends | Change from base | Accounting checks |
|---|---|---:|---:|---:|---:|---|
| Lower | 5.0%, 4.0%, 3.0%, 2.0%, 2.0% | 3,500.8 | -212.6 | 2,512.5 | -156.0 | PASS FY2026E-FY2030E; each balance-sheet gap rounds to 0.0 |
| Base | 6.0%, 5.0%, 4.0%, 3.0%, 3.0% | 3,713.4 | +0.0 | 2,668.5 | +0.0 | PASS FY2026E-FY2030E; each balance-sheet gap rounds to 0.0 |
| Higher | 7.0%, 6.0%, 5.0%, 4.0%, 4.0% | 3,934.4 | +221.0 | 2,830.1 | +161.6 | PASS FY2026E-FY2030E; each balance-sheet gap rounds to 0.0 |
| **Span** | maximum minus minimum | **433.6** |  | **317.7** |  | Valid runs only |

### Compensation-to-revenue sensitivity

| Case | Actual compensation / revenue input | FY2030 operating profit | Change from base | FY2030 FCFE before dividends | Change from base | Accounting checks |
|---|---|---:|---:|---:|---:|---|
| Lower | 55.9% in FY2026E-FY2030E | 3,882.6 | +169.2 | 2,804.4 | +135.9 | PASS FY2026E-FY2030E; each balance-sheet gap rounds to 0.0 |
| Base | 56.9% in FY2026E-FY2030E | 3,713.4 | +0.0 | 2,668.5 | +0.0 | PASS FY2026E-FY2030E; each balance-sheet gap rounds to 0.0 |
| Higher | 57.9% in FY2026E-FY2030E | 3,544.2 | -169.2 | 2,532.6 | -135.9 | PASS FY2026E-FY2030E; each balance-sheet gap rounds to 0.0 |
| **Span** | maximum minus minimum | **338.4** |  | **271.8** |  | Valid runs only |

### Selected-result statement trace

This trace shows the full linked path to the revenue-growth higher result in
FY2030E. It demonstrates that the $221.0m change in operating profit is not a
typed output.

| FY2030E, revenue-growth higher case | USD millions |
|---|---:|
| Revenue before reimbursements | 17,747.3 |
| Compensation | (10,101.2) |
| Operating expense | (2,908.5) |
| Depreciation | (163.2) |
| Amortization | (640.0) |
| Operating profit (EBIT) | 3,934.4 |
| Net income | 2,729.0 |
| FCFE before dividends | 2,830.1 |
| Cash and equivalents | 10,267.0 |

### Restored-base and valuation status

The final fresh base rerun matched the first base **exactly**: FY2030E operating
profit was $3,713.4m and FY2030E FCFE before dividends was $2,668.5m. The
FY2026E-FY2030E asset-less-liabilities-and-equity gaps were all 0.0 after
rounding and the minimum-cash check passed in every year.

**Value per share is unavailable for this Lab 11 ranking.** The existing Lab 10
calculation printed $100.82 per share, but it discounts FCFE less dividends.
That mixes an equity cash-flow measure with distributions to equity, so its
terminal-value convention must be reconciled before it is defensible to rank
per-share sensitivities. I retained signed FCFE and did not invent a terminal
value.

## E - Main driver over these ranges

**Over these stated ranges, organic revenue growth is the larger driver** of
both final-year operating profit and FCFE before dividends: its spans are
$433.6m and $317.7m, versus $338.4m and $271.8m for compensation / revenue.
This is not a claim that growth is inherently more important. A wider or
narrower chosen range could change the ranking.

The causal link is: growth increases revenue; fixed compensation and operating
expense ratios leave a contribution margin; then higher receivables and other
operating assets absorb some cash, and taxes increase. That is why the revenue
case raises EBIT more than FCFE. The result does not change the valuation
conclusion because per-share value remains unresolved; it raises the research
priority of checking AJG's organic-growth evidence and renewal/new-business
trends.

## Sensitivity — Learn on your own

1. **One-at-a-time sensitivity** reruns the same linked model after changing
one independent input while holding every other independent assumption at its
base value. It measures the model's conditional response, not a combined
scenario.
2. The chosen range affects the ranking because the output span is measured
across that range. A large span can come from a wide input range as well as a
large underlying relationship.
3. A sensitivity table is **not a forecast probability**. It contains selected
possibilities, has no stated likelihoods or probability weights, and does not
show correlations or simultaneous changes among assumptions.

## Reflection

Revenue growth mattered most over my tested ranges. The surprising result was
how much of the EBIT improvement did not reach FCFE: the +1.0 percentage-point
growth path added $221.0m to FY2030 EBIT but $161.6m to FCFE because linked
working capital and taxes also changed.

## Files for GitHub

- [Lab 11 results](Lab%2011%20-%20AJG%20-%20Sensitivity%20Results.md)
- [Lab 11 sensitivity runner](ajg_lab11_sensitivity.py)

The runner reads the existing Lab 10 file `ajg_proforma.py` from the same
folder. It is a dependency rather than a new Lab 11 deliverable, so keep it in
the repository if it was not already uploaded with Lab 10. This working folder
is not currently a Git repository and has no configured GitHub remote, so add
the two Lab 11 files to your course repository and use that repository's file
links for the checkout.

*This is an undergraduate finance-modeling exercise, not investment advice.*
