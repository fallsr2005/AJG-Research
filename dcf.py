"""Five-year FCFF discounted cash flow model for Arthur J. Gallagher & Co. (USD millions)."""

# 2025 Form 10-K (filed February 17, 2026; all amounts USD millions):
# https://www.sec.gov/Archives/edgar/data/354190/000162828026008662/ajg-20251231.htm
# FCFF = operating cash flow + cash interest * (1 - effective tax rate) - capex
#      = 1,930 + 575 * (1 - 19.7%) - 145 = 2,246.7
starting_fcff = 2246.7

# Valuation assumptions (not reported 10-K figures; edit as needed).
growth_rates = [0.08, 0.06, 0.05, 0.04, 0.03]  # Years 1 through 5
wacc = 0.10
terminal_growth = 0.03

# Sensitivity assumptions used to show how the current AJG model responds to
# discount-rate and terminal-growth changes. These use the same operating and
# bridge inputs as the base case below.
wacc_values = [0.09, 0.10, 0.11]
terminal_growth_values = [0.02, 0.03, 0.04]

# 2025 Form 10-K balance-sheet and EPS inputs (USD millions, except shares).
# Cash reconciliation: $1,155 non-restricted cash + $241 restricted cash =
# $1,396 total cash. Use only non-restricted cash in this bridge.
non_operating_cash = 1155.0
# Balance-sheet corporate-related borrowings: $640 current + $12,104 noncurrent.
# This is a carrying-amount convention. It differs from Note 7's $13,099
# gross corporate-and-other-debt figure, which includes the premium-financing
# facility; do not combine the two conventions in one bridge.
debt = 12744.0
# 2025 diluted weighted-average common and common-equivalent shares outstanding.
diluted_shares = 260.1


def value_per_diluted_share_for(wacc_value, terminal_growth_value):
    """Calculate one per-share DCF value using the current model inputs."""
    if terminal_growth_value >= wacc_value:
        return None

    current_fcff = starting_fcff
    discounted_fcff = 0.0
    for year, growth_rate in enumerate(growth_rates, start=1):
        current_fcff *= 1 + growth_rate
        discounted_fcff += current_fcff / (1 + wacc_value) ** year

    terminal_value = current_fcff * (1 + terminal_growth_value) / (
        wacc_value - terminal_growth_value
    )
    present_value_terminal = terminal_value / (1 + wacc_value) ** len(growth_rates)
    enterprise_value = discounted_fcff + present_value_terminal
    equity_value = enterprise_value + non_operating_cash - debt
    return equity_value / diluted_shares


def print_sensitivity_grid():
    """Print a terminal-readable per-share sensitivity grid."""
    headers = [f"{growth:.0%}" for growth in terminal_growth_values]
    print("\nSensitivity: Value per Diluted Share")
    print("WACC \\ terminal growth | " + " | ".join(headers))
    print("--- | " + " | ".join("---:" for _ in headers))

    for wacc_value in wacc_values:
        row = []
        for growth_value in terminal_growth_values:
            result = value_per_diluted_share_for(wacc_value, growth_value)
            row.append("invalid" if result is None else f"${result:.2f}")
        print(f"{wacc_value:.0%} | " + " | ".join(row))


def main():
    if len(growth_rates) != 5:
        raise SystemExit("Error: enter exactly five yearly growth rates.")
    if terminal_growth >= wacc:
        raise SystemExit(
            "Error: terminal growth must be less than WACC; the Gordon-growth formula is invalid otherwise."
        )
    if diluted_shares <= 0:
        raise SystemExit("Error: diluted shares must be greater than zero.")

    fcff = []
    current_fcff = starting_fcff
    for growth_rate in growth_rates:
        current_fcff *= 1 + growth_rate
        fcff.append(current_fcff)

    present_value_explicit_fcff = sum(
        cash_flow / (1 + wacc) ** year
        for year, cash_flow in enumerate(fcff, start=1)
    )
    terminal_value_year_5 = fcff[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    present_value_terminal_value = terminal_value_year_5 / (1 + wacc) ** 5
    enterprise_value = present_value_explicit_fcff + present_value_terminal_value
    equity_value = enterprise_value + non_operating_cash - debt
    value_per_diluted_share = equity_value / diluted_shares
    pv_terminal_value_share_of_ev = present_value_terminal_value / enterprise_value

    for year, cash_flow in enumerate(fcff, start=1):
        print(f"FCFF Year {year}: {cash_flow:.4f}")
    print(f"Present Value of Five Explicit FCFF: {present_value_explicit_fcff:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value_year_5:.4f}")
    print(f"Present Value of Terminal Value: {present_value_terminal_value:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {value_per_diluted_share:.4f}")
    print(f"PV Terminal Value as Share of Enterprise Value: {pv_terminal_value_share_of_ev:.4f}")
    print_sensitivity_grid()


if __name__ == "__main__":
    main()
