# Lab 09 — ABG Pro-Forma Build

Files submitted: `proforma.py` and this note. Amounts are USD millions except per-share values.

## Question

What are five years of a company's statements worth, built from assumptions that can be defended, and how do we know the statements are right?

The answer is a fully linked three-statement forecast whose assumptions are labeled by source and whose annual balance-sheet and minimum-cash checks must pass before it will value equity.

## Three judgments and cash last

The three value-carrying judgments are 1.8% organic revenue growth, 17.05% gross margin, and SG&A as a percentage of gross profit (66.5% in 2026, declining to 64.5%). They determine the operating profit and cash generation that the valuation discounts.

Cash is last because it is the residual result of operating performance, investment, working-capital movements, financing, and shareholder distributions. Calculating cash first would hide whether all other balance-sheet changes reconcile; calculating it last makes the balance sheet a check on the entire engine.

## Assumption labels

- Judgment: organic growth, gross margin, SG&A/gross profit, impairment, tax rate, other working capital, revolver rate, debt repayment, share buyback, cost of equity, and terminal growth.
- History: depreciation/opening PP&E, inventory days, floor-plan/inventory, minimum cash, revolver limit, floor-plan interest, and term-debt interest.
- Guidance: annual capital spending.
- Fact: 17.951349 million shares outstanding at 30 June 2026.

The FY2025 opening balance sheet and every numerical assumption are embedded in `proforma.py` exactly as supplied in the lab.

## Floor plan

Floor plan is inventory financing provided by manufacturers' finance arms and banks. It rises with inventory; the model calculates its interest on the opening balance, then includes the annual change in floor plan in FCFE as an operating source or use of cash. Removing it eliminates the financing that offsets the substantial inventory balance, so cash falls to roughly negative $1.1 billion in the video case.

## Validation

Running `python proforma.py` prints all three statements, the check block, and valuation. The model matches the supplied 2026 and 2030 known-answer lines to one decimal and returns approximately 80% of equity value after 2030. `assert_balanced` raises an error before valuation if assets less liabilities less equity is not zero or cash is below the minimum.

To perform the deliberate break test, replace the FY2026 cash assignment temporarily with `cash[year] = cash[prior]` for that year. The check must refuse FY2026E with a -61.4 gap, which is the change in cash with its sign reversed. Undo that test edit afterward.
