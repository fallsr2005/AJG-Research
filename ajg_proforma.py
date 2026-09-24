"""Lab 10: Arthur J. Gallagher & Co. (AJG) five-year pro-forma.

USD millions except per-share values.  FY2025 is the opening, reported balance
sheet.  This is an organic, no-new-acquisitions forecast: acquisition activity
is a named, separate input rather than being hidden inside reported growth.
"""

from math import isclose


# Assumption set; labels and reasons are documented in Lab 10 - AJG - Pro-Forma.md.
REVENUE_GROWTH = {2026: 0.060, 2027: 0.050, 2028: 0.040, 2029: 0.030, 2030: 0.030}  # judgment
COMP_TO_REVENUE = 7_842 / 13_778       # history: FY2025 compensation / revenue before reimbursements
OPERATING_TO_REVENUE = 2_258 / 13_778  # history: FY2025 operating expense / revenue before reimbursements
AR_DAYS = 5_175 / 13_778 * 365         # history: FY2025 accounts receivable days
OTHER_CURRENT_TO_REVENUE = 886 / 13_778  # history
ACCRUED_TO_REVENUE = 4_017 / 13_778      # history
DEFERRED_REVENUE_TO_REVENUE = (737 + 155) / 13_778  # history
DEP_TO_OPENING_PPE = 206 / 789            # history
AMORT_TO_OPENING_INTANGIBLES = 916 / 10_684  # history
CAPEX = 145.0                              # history: FY2025 cash-flow capex; held flat
ACQUISITION_SPEND = {year: 0.0 for year in range(2026, 2031)}  # judgment: no new deals in base case
ACQUISITION_ASSET_SPLIT = (0.60, 0.40)     # judgment: goodwill, amortizable intangibles if a deal is added
TAX_RATE = 368 / 1_871                     # history: FY2025 provision / pretax income
CORPORATE_DEBT_REPAYMENT = 500.0            # judgment
DIVIDEND_GROWTH = 0.03                     # judgment
CORPORATE_DEBT_RATE = 0.050                 # judgment
MIN_CASH = 500.0                            # judgment
REVOLVER_LIMIT, REVOLVER_RATE = 1_000.0, 0.060  # judgment
COST_OF_EQUITY, TERMINAL_GROWTH = 0.090, 0.025  # judgment
SHARES_OUTSTANDING = 257.0                  # fact: FY2025 shares issued and outstanding, in millions

YEARS = list(range(2026, 2031))
OPENING_YEAR = 2025

# FY2025 opening balance sheet.  Fiduciary assets and liabilities are shown
# explicitly because they offset; they are client funds, not valuation cash.
revenue = {2025: 13_778.0}  # revenue before reimbursements
cash = {2025: 1_396.0}
fiduciary_assets = {2025: 26_899.0}
accounts_receivable = {2025: 5_175.0}
ppe = {2025: 789.0}
goodwill = {2025: 22_593.0}
intangibles = {2025: 10_684.0}
other_assets = {2025: 3_129.0}  # other current + deferred tax + other noncurrent + ROU assets
fiduciary_liabilities = {2025: 26_899.0}
accrued_liabilities = {2025: 4_017.0}
deferred_revenue = {2025: 892.0}
premium_finance_debt = {2025: 226.0}
corporate_debt = {2025: 12_744.0}
other_liabilities = {2025: 2_540.0}  # lease + other noncurrent liabilities
equity = {2025: 23_347.0}
revolver = {2025: 0.0}
dividends = {2025: 667.0}

compensation, operating_expense, depreciation, amortization = {}, {}, {}, {}
interest, pretax, tax, net_income, fcfe = {}, {}, {}, {}, {}


def assert_balanced(year, gap, year_end_cash):
    """Refuse valuation if a link is broken or liquidity is not funded."""
    if not isclose(gap, 0.0, abs_tol=1e-7):
        raise AssertionError(f"FY{year}E is not balanced: gap {gap:.1f}")
    if year_end_cash < MIN_CASH - 1e-7:
        raise AssertionError(f"FY{year}E cash is below the minimum: {year_end_cash:.1f} < {MIN_CASH:.1f}")


for year in YEARS:
    prior = year - 1
    revenue[year] = revenue[prior] * (1 + REVENUE_GROWTH[year])
    compensation[year] = revenue[year] * COMP_TO_REVENUE
    operating_expense[year] = revenue[year] * OPERATING_TO_REVENUE
    depreciation[year] = ppe[prior] * DEP_TO_OPENING_PPE
    amortization[year] = intangibles[prior] * AMORT_TO_OPENING_INTANGIBLES
    interest[year] = (corporate_debt[prior] * CORPORATE_DEBT_RATE
                      + revolver[prior] * REVOLVER_RATE)
    pretax[year] = (revenue[year] - compensation[year] - operating_expense[year]
                    - depreciation[year] - amortization[year] - interest[year])
    tax[year] = max(0.0, pretax[year]) * TAX_RATE
    net_income[year] = pretax[year] - tax[year]

    # Operating balance-sheet links.
    accounts_receivable[year] = revenue[year] * AR_DAYS / 365
    other_assets[year] = other_assets[prior] + (revenue[year] - revenue[prior]) * OTHER_CURRENT_TO_REVENUE
    ppe[year] = ppe[prior] + CAPEX - depreciation[year]
    goodwill[year] = goodwill[prior] + ACQUISITION_SPEND[year] * ACQUISITION_ASSET_SPLIT[0]
    intangibles[year] = (intangibles[prior] - amortization[year]
                          + ACQUISITION_SPEND[year] * ACQUISITION_ASSET_SPLIT[1])
    fiduciary_assets[year] = fiduciary_assets[prior]
    fiduciary_liabilities[year] = fiduciary_liabilities[prior]
    accrued_liabilities[year] = revenue[year] * ACCRUED_TO_REVENUE
    deferred_revenue[year] = revenue[year] * DEFERRED_REVENUE_TO_REVENUE
    premium_finance_debt[year] = premium_finance_debt[prior]
    other_liabilities[year] = other_liabilities[prior]
    corporate_debt[year] = corporate_debt[prior] - CORPORATE_DEBT_REPAYMENT
    dividends[year] = dividends[prior] * (1 + DIVIDEND_GROWTH)
    equity[year] = equity[prior] + net_income[year] - dividends[year]

    # Cash is last.  The additions/subtractions reconcile to the asset and
    # liability links above; no cash is typed to make the balance sheet work.
    fcfe[year] = (net_income[year] + depreciation[year] + amortization[year]
                  - CAPEX - (accounts_receivable[year] - accounts_receivable[prior])
                  - (other_assets[year] - other_assets[prior])
                  + (accrued_liabilities[year] - accrued_liabilities[prior])
                  + (deferred_revenue[year] - deferred_revenue[prior])
                  - ACQUISITION_SPEND[year] - CORPORATE_DEBT_REPAYMENT)
    cash_before_revolver = cash[prior] + fcfe[year] - dividends[year]
    if cash_before_revolver < MIN_CASH:
        draw = min(REVOLVER_LIMIT - revolver[prior], MIN_CASH - cash_before_revolver)
        revolver[year] = revolver[prior] + draw
        cash[year] = cash_before_revolver + draw
    else:
        repayment = min(revolver[prior], cash_before_revolver - MIN_CASH)
        revolver[year] = revolver[prior] - repayment
        cash[year] = cash_before_revolver - repayment


def total_assets(year):
    return (cash[year] + fiduciary_assets[year] + accounts_receivable[year] + ppe[year]
            + goodwill[year] + intangibles[year] + other_assets[year])


def liabilities_and_equity(year):
    return (fiduciary_liabilities[year] + accrued_liabilities[year] + deferred_revenue[year]
            + premium_finance_debt[year] + corporate_debt[year] + revolver[year]
            + other_liabilities[year] + equity[year])


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'USD millions':<32}" + "".join(f"{'FY' + str(y) + 'E':>12}" for y in YEARS))
    for label, values in rows:
        print(f"{label:<32}" + "".join(f"{values[y]:>12.1f}" for y in YEARS))


print_table("Income statement", [
    ("Revenue before reimbursements", revenue), ("Compensation", compensation),
    ("Operating expense", operating_expense), ("Depreciation", depreciation),
    ("Amortization", amortization), ("Interest", interest), ("Pretax income", pretax),
    ("Tax", tax), ("Net income", net_income),
])
print_table("Balance sheet", [
    ("Cash and equivalents", cash), ("Fiduciary assets", fiduciary_assets),
    ("Accounts receivable", accounts_receivable), ("PP&E", ppe), ("Goodwill", goodwill),
    ("Amortizable intangibles", intangibles), ("Other assets", other_assets),
    ("Total assets", {y: total_assets(y) for y in YEARS}),
    ("Fiduciary liabilities", fiduciary_liabilities), ("Accrued liabilities", accrued_liabilities),
    ("Deferred revenue", deferred_revenue), ("Premium-finance debt", premium_finance_debt),
    ("Corporate debt", corporate_debt), ("Revolver", revolver), ("Other liabilities", other_liabilities),
    ("Equity", equity),
])
print_table("Cash flow to equity", [
    ("Net income", net_income), ("Depreciation", depreciation), ("Amortization", amortization),
    ("Capital spending", {y: CAPEX for y in YEARS}),
    ("Change in receivables", {y: accounts_receivable[y] - accounts_receivable[y - 1] for y in YEARS}),
    ("Change in other assets", {y: other_assets[y] - other_assets[y - 1] for y in YEARS}),
    ("Change in accrued liabilities", {y: accrued_liabilities[y] - accrued_liabilities[y - 1] for y in YEARS}),
    ("Change in deferred revenue", {y: deferred_revenue[y] - deferred_revenue[y - 1] for y in YEARS}),
    ("Acquisition spending", ACQUISITION_SPEND),
    ("Corporate debt repayment", {y: CORPORATE_DEBT_REPAYMENT for y in YEARS}),
    ("FCFE before dividends", fcfe), ("Dividends", dividends),
])

print("\nChecks")
for year in YEARS:
    gap = total_assets(year) - liabilities_and_equity(year)
    print(f"FY{year}E: assets - liabilities - equity = {gap:.1f}; "
          f"cash >= minimum = {cash[year] >= MIN_CASH}; revolver = {revolver[year]:.1f}")
    assert_balanced(year, gap, cash[year])

# Valuation only runs after every balance-sheet and cash check passes.
pv_fcfe = sum((fcfe[y] - dividends[y]) / (1 + COST_OF_EQUITY) ** (y - OPENING_YEAR) for y in YEARS)
terminal_fcfe = fcfe[2030] - dividends[2030]
terminal_value = terminal_fcfe * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
pv_terminal_value = terminal_value / (1 + COST_OF_EQUITY) ** 5
equity_value = pv_fcfe + pv_terminal_value
value_per_share = equity_value / SHARES_OUTSTANDING

print("\nEquity valuation")
print(f"Equity value: ${equity_value:,.1f} million")
print(f"Share of value after 2030: {pv_terminal_value / equity_value:.1%}")
print(f"Value per share: ${value_per_share:,.2f}")
