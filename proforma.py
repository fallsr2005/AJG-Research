"""Lab 09: ABG five-year pro-forma three-statement model (USD millions)."""

from math import isclose


# Assumptions — labels distinguish judgment, history/guidance, and fact.
GROWTH = 0.018                         # judgment
GROSS_MARGIN = 0.1705                   # judgment
SGA_TO_GP = {2026: 0.665, 2027: 0.655, 2028: 0.645,
             2029: 0.645, 2030: 0.645} # judgment
DEP_TO_OPENING_PPE = 82.4 / 3_070.4     # history
IMPAIRMENT = 120.0                      # judgment; non-cash
CAPEX = 250.0                            # guidance
TAX_RATE = 0.255                         # judgment
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365  # history
FLOOR_PLAN_TO_INVENTORY = 2_027.0 / 2_135.8             # history
OTHER_WC_TO_REVENUE_CHANGE = 0.008       # judgment
MIN_CASH, REVOLVER_LIMIT, REVOLVER_RATE = 25.0, 850.0, 0.06
DEBT_REPAYMENT = 150.0                   # judgment
BUYBACK = 150.0                          # judgment
FLOOR_PLAN_RATE, TERM_DEBT_RATE = 0.0467, 0.0544  # history
COST_OF_EQUITY, TERMINAL_GROWTH = 0.10, 0.025    # judgment
SHARES_OUTSTANDING = 17.951349           # fact; millions

YEARS = list(range(2026, 2031))
OPENING_YEAR = 2025

# FY2025 opening balance sheet (USD millions).
revenue = {OPENING_YEAR: 17_999.0}
inventory = {OPENING_YEAR: 2_135.8}
ppe = {OPENING_YEAR: 3_070.4}
other_assets = {OPENING_YEAR: 6_371.6}
cash = {OPENING_YEAR: 40.4}
floor_plan = {OPENING_YEAR: 2_027.0}
term_debt = {OPENING_YEAR: 3_572.0}
other_liabilities = {OPENING_YEAR: 2_127.5}
equity = {OPENING_YEAR: 3_891.7}
revolver = {OPENING_YEAR: 0.0}

gross_profit, sga, depreciation, impairment = {}, {}, {}, {}
operating_income, interest, pretax, tax, net_income = {}, {}, {}, {}, {}
other_working_capital, fcfe = {}, {}


def assert_balanced(year, gap, year_end_cash):
    """Refuse valuation when a projected balance sheet or cash check fails."""
    if not isclose(gap, 0.0, abs_tol=1e-7):
        raise AssertionError(f"FY{year}E is not balanced: gap {gap:.1f}")
    if year_end_cash < MIN_CASH - 1e-7:
        raise AssertionError(
            f"FY{year}E cash is below the minimum: {year_end_cash:.1f} < {MIN_CASH:.1f}"
        )


for year in YEARS:
    prior = year - 1

    # Income statement, calculated from opening balances where instructed.
    revenue[year] = revenue[prior] * (1 + GROWTH)
    gross_profit[year] = revenue[year] * GROSS_MARGIN
    sga[year] = gross_profit[year] * SGA_TO_GP[year]
    depreciation[year] = ppe[prior] * DEP_TO_OPENING_PPE
    impairment[year] = IMPAIRMENT
    operating_income[year] = (gross_profit[year] - sga[year]
                               - depreciation[year] - impairment[year])
    interest[year] = (floor_plan[prior] * FLOOR_PLAN_RATE
                      + term_debt[prior] * TERM_DEBT_RATE
                      + revolver[prior] * REVOLVER_RATE)
    pretax[year] = operating_income[year] - interest[year]
    tax[year] = max(0.0, pretax[year]) * TAX_RATE
    net_income[year] = pretax[year] - tax[year]

    # Balance sheet, except cash and revolver.
    inventory[year] = ((revenue[year] - gross_profit[year])
                       * INVENTORY_DAYS / 365)
    floor_plan[year] = inventory[year] * FLOOR_PLAN_TO_INVENTORY
    ppe[year] = ppe[prior] + CAPEX - depreciation[year]
    other_working_capital[year] = OTHER_WC_TO_REVENUE_CHANGE * (revenue[year] - revenue[prior])
    other_assets[year] = other_assets[prior] + other_working_capital[year] - impairment[year]
    term_debt[year] = term_debt[prior] - DEBT_REPAYMENT
    other_liabilities[year] = other_liabilities[prior]
    equity[year] = equity[prior] + net_income[year] - BUYBACK

    # Cash flow to equity, then liquidity revolver. Cash is deliberately last.
    fcfe[year] = (net_income[year] + depreciation[year] + impairment[year]
                  - CAPEX - (inventory[year] - inventory[prior])
                  - other_working_capital[year]
                  + (floor_plan[year] - floor_plan[prior]) - DEBT_REPAYMENT)
    cash_before_revolver = cash[prior] + fcfe[year] - BUYBACK
    if cash_before_revolver < MIN_CASH:
        draw = min(REVOLVER_LIMIT - revolver[prior], MIN_CASH - cash_before_revolver)
        revolver[year] = revolver[prior] + draw
        cash[year] = cash_before_revolver + draw
    else:
        repayment = min(revolver[prior], cash_before_revolver - MIN_CASH)
        revolver[year] = revolver[prior] - repayment
        cash[year] = cash_before_revolver - repayment


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'USD millions':<30}" + "".join(f"{'FY' + str(y) + 'E':>12}" for y in YEARS))
    for label, values in rows:
        print(f"{label:<30}" + "".join(f"{values[y]:>12.1f}" for y in YEARS))


print_table("Income statement", [
    ("Revenue", revenue), ("Gross profit", gross_profit), ("SG&A", sga),
    ("Depreciation", depreciation), ("Impairment", impairment),
    ("Operating income", operating_income), ("Interest", interest),
    ("Pretax income", pretax), ("Tax", tax), ("Net income", net_income),
])
print_table("Balance sheet", [
    ("Inventory", inventory), ("PP&E", ppe), ("Other assets", other_assets),
    ("Cash", cash), ("Total assets", {y: inventory[y] + ppe[y] + other_assets[y] + cash[y] for y in YEARS}),
    ("Floor plan", floor_plan), ("Term debt", term_debt), ("Revolver", revolver),
    ("Other liabilities", other_liabilities), ("Equity", equity),
])
print_table("Cash flow", [
    ("Net income", net_income), ("Depreciation", depreciation), ("Impairment", impairment),
    ("Capital spending", {y: CAPEX for y in YEARS}),
    ("Change in inventory", {y: inventory[y] - inventory[y - 1] for y in YEARS}),
    ("Change in other working capital", other_working_capital),
    ("Change in floor plan", {y: floor_plan[y] - floor_plan[y - 1] for y in YEARS}),
    ("Debt repayment", {y: DEBT_REPAYMENT for y in YEARS}), ("FCFE", fcfe),
])

print("\nChecks")
for year in YEARS:
    assets = inventory[year] + ppe[year] + other_assets[year] + cash[year]
    liabilities_and_equity = (floor_plan[year] + term_debt[year] + revolver[year]
                              + other_liabilities[year] + equity[year])
    gap = assets - liabilities_and_equity
    print(f"FY{year}E: assets - liabilities - equity = {gap:.1f}; "
          f"cash >= minimum = {cash[year] >= MIN_CASH}")
    assert_balanced(year, gap, cash[year])

# Valuation happens only after all balance-sheet checks pass.
pv_fcfe = sum(fcfe[year] / (1 + COST_OF_EQUITY) ** (year - OPENING_YEAR) for year in YEARS)
terminal_value = ((fcfe[2030] + DEBT_REPAYMENT) * (1 + TERMINAL_GROWTH)
                  / (COST_OF_EQUITY - TERMINAL_GROWTH))
pv_terminal_value = terminal_value / (1 + COST_OF_EQUITY) ** 5
equity_value = pv_fcfe + pv_terminal_value
value_per_share = equity_value / SHARES_OUTSTANDING

print("\nEquity valuation")
print(f"Equity value: ${equity_value:,.1f} million")
print(f"Share of value after 2030: {pv_terminal_value / equity_value:.1%}")
print(f"Value per share: ${value_per_share:,.2f}")
