# Project 2 — Investment Mandate

This classroom mandate was created October 22, 2026 because the earlier saved Lab 13 work covered Meridian, not a separate personal Project 2 mandate. Its target and constraint are classroom assumptions, not a real investment recommendation.

## Purpose and objective

Construct a diversified, long-only portfolio from four exchange-traded funds and find the lowest estimated-volatility mix that meets an **estimated annual return of at least 6.0%**. This is a nominal, forward-looking classroom target, not a promised return. Use estimates from the available monthly adjusted-price history as inputs, explicitly labeling them as historical estimates rather than forecasts.

## Hard constraint

Hold **at least 10% of the portfolio in SGOV** as a short-term Treasury-bill reserve. For this classroom model, SGOV is the sole reserve-eligible fund. The 10% threshold is a classroom design choice, not a calculated spending requirement. The portfolio weights must be nonnegative and sum to 100%; no borrowing or short positions are modeled.

## Permitted universe

| Ticker | Fund | Portfolio role |
|---|---|---|
| SGOV | iShares 0–3 Month Treasury Bond ETF | Treasury-bill reserve |
| SCHR | Schwab Intermediate-Term U.S. Treasury ETF | Intermediate-term government bonds |
| USIG | iShares Broad USD Investment Grade Corporate Bond ETF | Investment-grade corporate bonds |
| ACWI | iShares MSCI ACWI ETF | Global equities |

## Defense and limitations

The 6.0% objective sets a measurable hurdle for comparing mixes; the 10% reserve preserves a defined liquid sleeve. Minimizing volatility among portfolios satisfying both addresses risk without assuming that the highest historical return is the best choice. Higher equity exposure may be necessary to meet the target, and the target may become infeasible under different estimates. Historical returns, volatility, and correlation are uncertain; a one-percentage-point sensitivity check can reveal dependence on a single estimate. The reserve fund can fluctuate and is not cash or a guaranteed loss limit. This simplified mandate does not specify spending needs, taxes, turnover, maximum drawdown, or a benchmark, and the model must not claim to check those rules.

