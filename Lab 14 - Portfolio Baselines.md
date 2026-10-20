# Lab 14 — Portfolio Baselines

## Question and assumptions

What does each simple portfolio earn and risk, and does any meet the Meridian mandate? The return and volatility inputs are course-authored training assumptions, not market estimates. The expected-return objective is 6.5%, calculated as estimated CPI of 2.5% plus 4%. The actual mandate specifies a net-of-cost return over rolling five-year periods; the simple annual estimates below do not establish that outcome.

Run `python portfolio.py` for the baseline results and `python 14_mandate.py` for the checkable mandate rules. Returns, volatilities, and correlations in the engine are expressed as decimals. Volatility is an annual standard deviation, not a maximum loss.

| Portfolio | Bills / 10-year / IG / equity | Expected return | Volatility | Reserve eligible | Meets 6.5% return target? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

The benchmark is the only baseline reaching the simple return target, but candidate E fails the 3.0% minimum reserve rule. The other two meet the reserve minimum but fall short of the return target. None both reaches the estimated return target and passes the reserve rule. Full mandate compliance also depends on other rules and the unresolved calendar-year-loss definition; these estimates cannot prove it.

## Verification

- The original Lab 13 checker returned A and D passing every checkable rule, B failing three, and C failing one. Adding E produced a 0.0% reserve, below 3.0%, and a failure of one checkable rule. The calendar-year loss rule remains unresolved.
- The engine reproduced all the known-answer values above. Changing both IG–equity correlation entries from 0.25 to 0.50 yielded benchmark volatility of 11.00%. The saved input remains 0.25 in both cells.
- A 1.3 IG–equity correlation was rejected with a message that correlations must be between -1 and 1. An asymmetric table was also rejected. These probes used copies of the inputs, leaving the saved table unchanged.

## Diversification and hand calculation

Diversification spreads a portfolio across assets whose returns do not move perfectly together. When correlation is below +1, movements can partly offset each other, reducing the portfolio's variance relative to the same weighted assets moving in perfect lockstep. This does not guarantee that the combined volatility is below both individual volatilities; the weights, volatilities, and correlation all matter.

For the benchmark, with weights 0.4 and 0.6, volatilities 0.06 and 0.16, and correlation 0.25:

`variance = (0.4 × 0.06)² + (0.6 × 0.16)² + 2 × 0.4 × 0.6 × 0.06 × 0.16 × 0.25`

`= 0.000576 + 0.009216 + 0.001152 = 0.010944`

`volatility = √0.010944 = 0.10461 = 10.46%`.

The double sum in `portfolio_volatility` includes each asset's own variance and both ordered cross-asset covariance terms. The covariance matrix first converts each correlation into `correlation × volatility_i × volatility_j`; the square root converts the weighted variance back to volatility.

## Partner discussion notes

My partner agreed with the explanation that diversification can reduce risk when assets do not move perfectly together. For the 40/60 benchmark, the calculation above gives 10.46% volatility: below equity's 16%, though above the bond fund's 6%.

For the code explanation, the covariance matrix combines correlations with both sleeve volatilities. The weighted double sum includes each sleeve's variance and each pair's covariance; its square root gives portfolio volatility. A partner question to discuss is why both IG–equity and equity–IG appear: together they provide the factor of two in the cross term of the hand calculation.

We completed the explanations and swapped roles. We discussed the two covariance cross terms, ran my partner's file and checked its known answers, then changed an IG–equity correlation to 1.3 and confirmed that the program refused it. We restored 0.25 and reran it successfully.

**AI quiz:** Why are both IG–equity and equity–IG covariance terms included? The code goes through every ordered pair of assets. The two terms are equal, so together they produce the factor of 2 in the cross term of the hand calculation.

## Reflection prompts

Inverse volatility places most weight in bills because their assumed 0.5% volatility is far below the other inputs; its reciprocal is consequently much larger. It does not directly optimize the expected return or account for correlation when choosing weights.

I would show the benchmark first because it is Meridian's stated comparison and is the only baseline above the simple target, while immediately flagging that its 0% reserve breaches the mandate. It is a diagnostic starting point, not an acceptable recommendation as stated.

## Thursday preparation: provisional fund universe

The following practice funds cover the course's four example roles. Confirm these roles against the actual Project 2 mandate before treating them as the final personal universe. These are examples, not recommendations.

| Ticker | Fund | Role | Adjusted-price source |
|---|---|---|---|
| BIL | State Street SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve proxy | [Yahoo Finance history](https://finance.yahoo.com/quote/BIL/history/) |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds | [Yahoo Finance history](https://finance.yahoo.com/quote/IEF/history/) |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade fixed income | [Yahoo Finance history](https://finance.yahoo.com/quote/LQD/history/) |
| VT | Vanguard Total World Stock ETF | Broad global equity | [Yahoo Finance history](https://finance.yahoo.com/quote/VT/history/) |

`prices.csv` contains 60 monthly adjusted close observations per ticker, October 2021–September 2026, downloaded October 20, 2026 from Yahoo Finance's chart endpoint by `download_prices.py`. The date is the first day of the labeled month; the value is Yahoo's monthly adjusted close for that month, not a price observed on that date. Adjusted closes incorporate distribution and split adjustments and may be revised by the provider. Months are oldest first, with matching observations and no missing values. The 60 observations produce 59 adjacent monthly returns; a full 60-month return series would require an additional preceding price.

## In-person and checkout items

The partner explanations, file-swap test, and AI quiz are recorded above. Confirm the provisional funds against the Project 2 mandate. Publish the files to your own GitHub repository and submit their links for checkout.
