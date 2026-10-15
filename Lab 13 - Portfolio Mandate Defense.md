# Lab 13 — Portfolio Mandate Defense

## What an investment policy statement is

An investment policy statement (IPS) is the written agreement that translates a client's purpose, return goal, risk tolerance, liquidity needs, time horizon, and governance into decision rules.  It guides portfolio design, implementation, monitoring, and rebalancing.  Objectives say what success means; constraints limit the eligible solution set.  A benchmark helps evaluate results but does not itself define an optimization objective.

## Sort and map the Meridian statements

| Statement | Type | Reason and IPS mapping |
|---|---|---|
| S1 — Seven-year horizon; annual rebalancing | Hard constraint | It sets the planning horizon and a required rebalancing cadence; these are time-horizon and governance/implementation terms. |
| S2 — CPI + 4% annually, net of costs, over rolling five-year periods | Objective | It defines the required real return, net-of-cost basis, and evaluation period. |
| S3 — $0.75m quarterly payout; 12 months held in cash or daily-liquid government securities | Hard constraint | This is a spending/liquidity rule that can be computed as a minimum reserve allocation. |
| S4 — 60% global equities / 40% U.S. investment-grade bonds benchmark | Preference | It is a performance comparison reference, not an instruction to hold those exact weights. |
| S5 — Long-only; no borrowing, short sales, or derivatives | Hard constraint | It restricts permitted instruments and leverage. |
| S6 — No single issuer above 8% | Hard constraint | It is a concentration limit; securities of one company must be aggregated. |
| S7 — Turnover at most 25% without committee approval | Hard constraint | It imposes an implementation limit, conditional on governance approval. |
| S8 — At least 90% redeemable within five business days | Hard constraint | It is a measurable liquidity constraint. |
| S9 — No calendar-year loss greater than 10%; no measure or breach rule | Unverifiable promise | The intended risk limit lacks a return measurement convention and an action if it is breached, so it must not be coded as a pass/fail rule. |
| S10 — No sector, ESG, tax, or home-bias preference; pilot objective unnamed | Missing | The optimization target has not been chosen; the absence of stated preferences does not tell us what to optimize. |

## Checker and known-answer verification

The standard-library checker is [mandate.py](mandate.py). Run it from this folder with:

```powershell
python mandate.py
```

It computes the 3.0% reserve minimum as `4 × $0.75m ÷ $100m × 100`. The results matched the provided answer: A passes every checkable rule; B fails reserve, liquidity, and aggregated Acme issuer exposure (9.0%); C fails reserve only. S9 is deliberately reported as `requires CIO clarification`, never tested.

### Negative-weight probe

I temporarily changed A's Cash weight from 2% to -2% and its global equity index fund weight from 60% to 64%, then reran the checker. A's lowest weight was -2.0 and failed long-only; the only other values remained compliant, including a 10.0% reserve allocation. I restored the original 2% Cash and 60% global-equity weights afterward.

### AI self-quiz

The line I checked was the issuer aggregation. Question: *Why does candidate B fail the issuer limit when no individual Acme holding exceeds 8%?* My answer: the mandate says one company's securities count together, so 5% Acme bonds plus 4% Acme stock equals 9%, above the 8% cap.

## Attack candidate D

Candidate D holds 4% Cash, 88% global equity index fund, and 8% Acme stock; all other holdings are 0%. It runs and passes every check in `mandate.py`: it is fully liquid within five business days, has a 4% reserve, and has 8% (not more than 8%) in Acme.

The objection holds because D's 96% equity exposure may be inconsistent with the intended calendar-year-loss protection. S9 decides it: passing code cannot establish compliance until the CIO defines the loss measure and breach response; I would cite S9 against a sceptical colleague's similarly high-risk passing portfolio.

## The CIO question before optimization

**Question:** What should the pilot optimize: minimum tracking error to the 60/40 benchmark, the probability of meeting CPI + 4% net over rolling five-year periods, or another stated risk-adjusted goal?

**Answer that changes the portfolio:** If the CIO answers “minimize tracking error to the 60/40 benchmark,” the portfolio should be built close to that benchmark (subject to the constraints), not like candidate D's 96% equity exposure. If the CIO instead prioritizes the probability of meeting CPI + 4% net, its asset mix and forecasts should be selected for that objective. This decision is required by S10.

## Reflection

A portfolio can pass every checkable rule yet still be wrong because the checker only enforces stated, measurable constraints. It cannot infer the intended risk tolerance, choose among competing objectives, forecast whether CPI + 4% is attainable net of costs, or resolve S9's undefined loss rule. Candidate D demonstrates that gap.

I was least sure about S4. I classified it as a preference because a benchmark is vital for evaluating performance, but its wording does not say the portfolio must track it or that tracking error is the pilot's objective. The CIO's answer to the S10 question determines whether it becomes a design target.
