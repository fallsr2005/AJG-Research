# Arthur J. Gallagher - Five-Year FCFF DCF Sensitivity and Reverse DCF

## Purpose

This companion note documents the sensitivity-grid and reverse-DCF extensions to the five-year FCFF valuation in `dcf.py`. It is a valuation diagnostic, not evidence of mispricing.

## Existing model inputs held fixed

Unless a grid cell or the reverse-DCF shift changes an item named below, hold these inputs fixed:

| Input | Current value | Treatment |
|---|---:|---|
| Starting FCFF | $2,246.7 million | Starting annual free cash flow to the firm |
| Explicit growth rates | 8.0%, 6.0%, 5.0%, 4.0%, 3.0% | Years 1-5; each receives the same reverse-DCF shift |
| WACC | 10.0% | Grid variable; otherwise fixed |
| Terminal growth | 3.0% | Grid variable; otherwise fixed |
| Non-operating cash | $1,155.0 million | Added in the enterprise-to-equity bridge |
| Debt | $12,744.0 million | Subtracted in the enterprise-to-equity bridge |
| Diluted shares | 260.1 million | Used to calculate value per diluted share |

The FCFF valuation sequence is:

1. Forecast FCFF for five years using the explicit growth rates.
2. Discount each forecast FCFF by WACC.
3. Calculate terminal value at Year 5 using the Gordon-growth formula: `FCFF_5 * (1 + g) / (WACC - g)`.
4. Add the present values to obtain enterprise value; add cash and subtract debt to obtain equity value.
5. Divide equity value by diluted shares.

## Sensitivity grid

Keep editable lists at the top of `dcf.py`:

```python
wacc_values = [0.09, 0.10, 0.11]
terminal_growth_values = [0.02, 0.03, 0.04]
```

Print a terminal-readable table below the model's existing twelve output lines. Rows are WACC values and columns are terminal-growth values. For each cell, recalculate only value per diluted share, holding all other inputs fixed. Mark a cell `invalid` when terminal growth is greater than or equal to WACC, because the Gordon-growth formula is not valid otherwise.
The expected training-case grid is:

| WACC \ terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | $28.60 | $32.94 | $39.02 |
| 10% | $24.36 | $27.50 | $31.69 |
| 11% | $21.06 | $23.41 | $26.44 |

The base case sits at the center. Values fall as WACC rises (moving down) and rise as terminal growth rises (moving right). Read the corners to understand the range created by the two assumptions.

## Reverse DCF

Set these editable inputs at the top of `dcf.py`:

```python
target_share_price = 30.00
reverse_shift_lower = -0.05
reverse_shift_upper = 0.10
```

Solve for one uniform shift added to every explicit annual growth rate. For a candidate shift `s`, the five rates become:

```text
[8%, 6%, 5%, 4%, 3%] + s
```

Use bisection within the stated lower and upper bounds. Reject a bracket before solving if either endpoint causes any annual growth rate to be -100% or lower. If the target share price is not bracketed by the values at valid endpoints, print `no solution in that bracket`; do not return an endpoint as an answer.

For every successful solve, print:

- the solved uniform growth-rate shift;
- the target share price;
- the inputs held fixed, including starting FCFF, base growth-rate list, WACC, terminal growth, cash, debt, diluted shares, and the search bounds.

For the supplied training case and a $30.00 target, the uniform shift should be approximately **+1.78 percentage points**. Label that output `training` until it is replaced with Arthur J. Gallagher inputs and a contemporaneous AJG market price.

### AJG reverse DCF solve: current documented inputs

For the $30.00 training target, the AJG inputs in this file do **not** produce a solution inside the allowed uniform-growth-shift bracket of -5.00% to +10.00%. The required output is therefore `no solution in that bracket`; returning either bound as the answer would be incorrect.

| Item | Result |
|---|---:|
| Target share price | $30.00 |
| Lower bound: uniform growth shift | -5.00% |
| Value per share at lower bound | $68.8520 |
| Upper bound: uniform growth shift | +10.00% |
| Value per share at upper bound | $166.1902 |
| Solved shift | No solution in that bracket |

**Inputs held fixed:** starting FCFF of $2,246.7 million; five base growth rates of 8.0%, 6.0%, 5.0%, 4.0%, and 3.0%; WACC of 10.0%; terminal growth of 3.0%; non-operating cash of $1,155.0 million; debt of $12,744.0 million; and 260.1 million diluted shares. This is `training target applied to AJG inputs`, not a finding of mispricing.

## Interpretation

A positive solved shift means the model needs higher explicit FCFF growth, under the assumptions held fixed, to reach the target price. A negative shift means it needs lower growth. Neither result alone establishes that AJG is under- or over-valued: it is conditional on the FCFF definition, WACC, terminal-growth rate, bridge items, shares, and target market price.

This is not investment advice. This is for educational purposes only. 
