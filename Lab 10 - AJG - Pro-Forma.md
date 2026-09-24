# Lab 10 - Pro-Forma: Arthur J. Gallagher & Co. (NYSE: AJG)

All dollars are USD millions except per-share data. The companion model is `ajg_proforma.py`.

## Reopen and rerun check

The original `proforma.py` was rerun before adapting it. Its ABG check block remained zero in FY2026E and FY2030E and it printed an ABG value of $291.75 per share. The AJG version is deliberately a new file, so the known-answer file remains available unchanged.

## D - Question and company-specific line

**Question:** What are five years of Arthur J. Gallagher's statements worth, built from assumptions I can defend?

AJG is an insurance broker and risk-management company: it earns commissions and fees rather than underwriting insurance risk. The line that makes it different in my model is **acquisition activity**. Its reported growth is not all organic because it buys brokerages; I model organic revenue growth separately and set new acquisition spending to zero in the base case. The FY2025 opening balance sheet already includes AssuredPartners, while future deals would otherwise add revenue, goodwill/intangibles, and financing that cannot be honestly buried in a single growth rate.

## R - Filing history

### History grid

“Revenue” below means revenue before reimbursements. Reimbursements have an equal expense and are excluded from the operating model. AJG sells services, not inventory: it has no reported cost of goods sold/gross-profit line and no inventory line. “SG&A” is therefore not reported; compensation plus operating expense is shown as the closest disclosed operating-cost proxy, not relabeled as fact.

| Item | FY2023 | FY2024 | FY2025 | Filing source for each year |
|---|---:|---:|---:|---|
| Revenue before reimbursements | 9,927 | 11,401 | 13,778 | 2023 10-K p. 70; 2024 10-K p. 70; 2025 10-K p. 70 |
| Gross profit | N/A - service brokerage, no COGS/gross-profit line | N/A | N/A | 2023 10-K p. 70; 2024 10-K p. 70; 2025 10-K p. 70 |
| Compensation + operating expense (SG&A proxy) | 7,370 | 8,276 | 10,100 | 2023 10-K p. 70; 2024 10-K p. 70; 2025 10-K p. 70 |
| Net earnings | 966 | 1,471 | 1,503 | 2023 10-K p. 70; 2024 10-K p. 70; 2025 10-K p. 70 |
| Inventory | N/A - no inventory reported | N/A | N/A | 2023 10-K p. 72; 2024 10-K p. 72; 2025 10-K p. 72 |
| PP&E (fixed assets, net) | 726.4 | 650.3 | 789.0 | 2023 10-K p. 72; 2024 10-K p. 72; 2025 10-K p. 72 |
| Total shareholders' equity | 10,815.3 | 20,180.0 | 23,347.0 | 2023 10-K p. 72; 2024 10-K p. 72; 2025 10-K p. 72 |

I checked FY2025 revenue before reimbursements ($13,778m) and FY2025 fixed assets, net ($789m) directly against the 2025 10-K statement pages (pp. 70 and 72). The same three-year income-statement amounts are also presented in the 2025 filing, which is why it is the primary source for the history grid. The earlier filings remain the source trail for each comparative balance-sheet year: [2023 10-K](https://www.sec.gov/Archives/edgar/data/354190/000095017024013370/ajg-20231231.htm), [2024 10-K](https://www.sec.gov/Archives/edgar/data/354190/000095017025021775/ajg-20241231.htm), and [2025 10-K](https://www.sec.gov/Archives/edgar/data/354190/000162828026008662/ajg-20251231.htm).

### Ratios and operating measures

| Measure | FY2023 | FY2024 | FY2025 | Source / calculation |
|---|---:|---:|---:|---|
| Gross margin | N/A | N/A | N/A | No reported COGS or gross profit for this service business |
| SG&A / gross profit | N/A | N/A | N/A | Neither item is reported by AJG |
| Accounts-receivable days (replacement for inventory days) | 137.3 | 123.1 | 135.5 | AR / revenue before reimbursements x 365; balance sheets and p. 70 |
| Inventory days | N/A | N/A | N/A | No inventory balance |
| Depreciation / ending PP&E | 22.7% | 27.4% | 26.1% | Depreciation / fixed assets, net |
| Capital spending: filing outflow / provider CapEx | (194) / (194) | (142) / (142) | (145) / (145) | 10-K cash-flow statements, p. 73; [StockAnalysis CapEx field](https://stockanalysis.com/stocks/ajg/financials/cash-flow-statement/) (S&P Global data) |
| Tax rate | 18.5% | 21.5% | 19.7% | Income-tax provision / pretax income, p. 70 |
| Reported total-revenue growth | 17.8% | 14.7% | 20.7% | Total revenues: 10,072 / 8,551; 11,555 / 10,072; 13,942 / 11,555 |
| Disclosed organic base commission-and-fee growth | 9% | 7% | 6% | 2023 10-K, p. 42; 2025 10-K, p. 45; non-GAAP measure |

Organic growth is growth from businesses owned in both periods, after excluding acquisition/divestiture and selected currency/variable items. AJG calls it “organic revenue change”; its 2025 MD&A says organic base commission-and-fee revenue grew 6%, while reported commission and fees grew 20%. That difference is precisely why my 6% FY2026 assumption is not the 20.7% reported top-line rate.

## Assumption set

| Value | Label | Reason |
|---|---|---|
| FY2026-FY2030 revenue growth: 6%, 5%, 4%, 3%, 3% | Judgment | I start with AJG's disclosed 6% FY2025 organic base commission-and-fee growth, then fade it as a mature brokerage. I do not count a new acquisition as organic growth. |
| Compensation / revenue before reimbursements: 56.9% | History | FY2025 compensation of $7,842m / $13,778m operating revenue. |
| Operating expense / revenue before reimbursements: 16.4% | History | FY2025 operating expense of $2,258m / $13,778m operating revenue. |
| Receivable days: 135.5 | History | FY2025 AR of $5,175m / $13,778m x 365. |
| Other-current-assets / revenue: 6.4% | History | FY2025 other current assets of $886m / $13,778m. |
| Accrued liabilities / revenue: 29.2% | History | FY2025 accrued compensation and other current liabilities of $4,017m / $13,778m. |
| Deferred revenue / revenue: 6.5% | History | FY2025 current plus noncurrent deferred revenue of $892m / $13,778m. |
| Depreciation / opening PP&E: 26.1% | History | FY2025 depreciation $206m / FY2025 PP&E $789m; applied to opening PP&E in the forecast. |
| Amortization / opening intangibles: 8.6% | History | FY2025 amortization $916m / FY2025 amortizable intangibles $10,684m. |
| Capital spending: $145m annually | History | FY2025 cash-flow capital expenditures; I hold it flat because management did not give an annual capex forecast in the 10-K. |
| Floor plan / inventory financing: none | Fact about model structure | AJG reports no inventory in its balance sheet and is a service broker, so there is no manufacturer-financed inventory line to forecast. The company-specific replacement is acquisition spending and related goodwill/intangible assets. |
| New acquisition spending: $0 | Judgment | The base case is a stand-alone organic forecast after the 2025 AssuredPartners deal. I would change this after a named acquisition, its price, expected revenue, and financing are disclosed. |
| Acquisition asset split: 60% goodwill / 40% intangibles | Judgment | This only applies if a future acquisition input is added. I use a transparent placeholder split rather than letting a deal disappear into “other assets.” |
| Tax rate: 19.7% | History | FY2025 provision $368m / pretax income $1,871m. |
| Corporate debt repayment: $500m annually | Judgment | I want the larger post-AssuredPartners debt balance to decline; I would change this if cash generation, refinancing, or acquisitions change. |
| Dividend growth: 3% | Judgment | I used a modest annual increase from FY2025 dividends paid of $667m, below the model's initial organic revenue assumption. |
| Corporate debt rate: 5.0% | Judgment | A rounded planning rate for the mixed debt stack; I would replace it with the weighted coupon/yield from a new debt note. |
| Minimum cash: $500m; revolver: $1,000m at 6% | Judgment | I keep a liquidity buffer and make any shortfall visible as a revolver draw rather than typing cash. |
| Cost of equity: 9.0%; terminal growth: 2.5% | Judgment | These are conservative long-run equity-cash-flow inputs. I would change them for a revised beta/risk-free-rate view or a different long-run nominal-growth view. |
| Shares outstanding: 257.0m | Fact | FY2025 balance sheet, p. 72. |

## I and V - Engine, checks, and price

The FY2025 opening balance sheet in `ajg_proforma.py` is taken from the 2025 10-K, p. 72. The model keeps fiduciary assets and liabilities visible and equal; they are client funds, not discretionary cash. It calculates cash last from net income, non-cash charges, capex, receivable/other-asset/liability changes, acquisition spending, debt repayment, and dividends. It therefore cannot use cash as an unexplained plug.

The check block prints an assets-less-liabilities-and-equity gap of **0.0 in FY2026E-FY2030E**, with cash above the $500m floor in each year. No year draws the revolver in this base case. `assert_balanced` stops before valuation if a balance-sheet link breaks or cash falls below the floor; I tested the refusal by replacing the FY2026 cash assignment in memory with `cash[prior]`. It stopped before valuation with `FY2026E is not balanced: gap -1439.5`.

On the same 257.0m share count, the model returns **$100.82 per share**. The market price was **$227.80 on September 24, 2026** (intraday observation; use the closing price if submitting after the close). The model says $100.82, while the market says $227.80, on the same share count: what mix of future acquired growth, margin improvement, and debt reduction is the market pricing that my organic-only base case leaves out? [Price source](https://www.investing.com/equities/arthur-j.-gallagher---co-historical-data)

## E - Partner review

**Partner question:** Your model uses 6% organic revenue growth in FY2026 but assumes no new acquisitions. Why is that number reasonable, and what evidence would make you change it?

**My answer:** I start at 6% because AJG disclosed 6% FY2025 organic growth in base commission and fee revenue, which excludes acquisition-driven revenue and is therefore a cleaner starting point than the 20.7% reported revenue-growth rate. I would lower or raise it if later MD&A showed a sustained change in client retention, new-business generation, renewal premium trends, or reported organic growth; I would model a new acquisition separately with its price and financing.

**My attack on my partner's model:** Which judgment is doing more work in your terminal value - your final-year cash flow or the terminal growth rate - and how would the filing make you lower it?

## Reflection

The label I would defend the longest is the **history** label on the 6% organic FY2026 starting point because it directly uses AJG's disclosed organic measure rather than mixing in acquisitions. The number that surprised me was the **$15.766bn FY2025 cash paid for acquisitions**: it makes clear why reported growth alone is not a cash-flow forecast.

*This is an undergraduate finance-modeling exercise, not investment advice.*
