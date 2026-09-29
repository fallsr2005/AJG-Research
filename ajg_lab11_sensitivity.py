"""Lab 11 one-at-a-time sensitivity analysis for AJG's existing Lab 10 model.

This runner executes a fresh copy of ajg_proforma.py for every case.  It does
not edit the Lab 10 base assumptions or reuse calculated statement values.
"""

from contextlib import redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
import re


MODEL_PATH = Path(__file__).with_name("ajg_proforma.py")
YEARS = tuple(range(2026, 2031))
BASE_GROWTH = {2026: 0.060, 2027: 0.050, 2028: 0.040, 2029: 0.030, 2030: 0.030}
BASE_COMP_TO_REVENUE = 7_842 / 13_778
GROWTH_SHIFT = 0.010  # 1.0 percentage point applied to each forecast year
COMP_SHIFT = 0.010    # 1.0 percentage point of revenue applied to each forecast year
CASES = ("Lower", "Base", "Higher")


def growth_path(shift):
    return {year: BASE_GROWTH[year] + shift for year in YEARS}


def fresh_model(revenue_growth, comp_to_revenue):
    """Execute the complete original model with only the specified inputs changed."""
    source = MODEL_PATH.read_text(encoding="utf-8")
    source, growth_count = re.subn(
        r"^REVENUE_GROWTH = .*$",
        f"REVENUE_GROWTH = {revenue_growth!r}  # Lab 11 one-at-a-time input",
        source,
        count=1,
        flags=re.MULTILINE,
    )
    source, comp_count = re.subn(
        r"^COMP_TO_REVENUE = .*$",
        f"COMP_TO_REVENUE = {comp_to_revenue!r}  # Lab 11 one-at-a-time input",
        source,
        count=1,
        flags=re.MULTILINE,
    )
    if growth_count != 1 or comp_count != 1:
        raise RuntimeError("Could not locate the two independent input lines in ajg_proforma.py.")
    namespace = {"__name__": "__lab11_model__", "__file__": str(MODEL_PATH)}
    with redirect_stdout(StringIO()):
        exec(compile(source, str(MODEL_PATH), "exec"), namespace)
    checks = {}
    for year in namespace["YEARS"]:
        gap = namespace["total_assets"](year) - namespace["liabilities_and_equity"](year)
        cash_ok = namespace["cash"][year] >= namespace["MIN_CASH"] - 1e-7
        checks[year] = {"gap": gap, "cash_ok": cash_ok, "pass": abs(gap) <= 1e-7 and cash_ok}
    return {"input_growth": revenue_growth, "input_comp": comp_to_revenue, "ns": namespace,
            "checks": checks, "valid": all(item["pass"] for item in checks.values())}


def metric(result):
    """Use EBIT and the model's explicitly labelled FCFE before dividends."""
    if not result["valid"]:
        return None
    ns = result["ns"]
    operating_profit = (ns["revenue"][2030] - ns["compensation"][2030] - ns["operating_expense"][2030]
                        - ns["depreciation"][2030] - ns["amortization"][2030])
    return {"operating_profit": operating_profit, "fcfe": ns["fcfe"][2030]}


def input_text(driver, result):
    if driver == "Revenue growth":
        return ", ".join(f"{year}: {result['input_growth'][year]:.1%}" for year in YEARS)
    return f"{result['input_comp']:.1%} of revenue (FY2026--FY2030)"


def checks_text(result):
    return "; ".join(
        f"{year}: gap {result['checks'][year]['gap']:.1f}, {'PASS' if result['checks'][year]['pass'] else 'FAIL'}"
        for year in YEARS
    )


def signed(value):
    return f"{value:+,.1f}"


def print_trace(driver, result):
    """Statement details sufficient to trace a selected linked result."""
    ns = result["ns"]
    print(f"\nTrace: {driver}, Higher case (FY2030E; USD millions)")
    rows = (("Revenue before reimbursements", "revenue"), ("Compensation", "compensation"),
            ("Operating expense", "operating_expense"), ("Depreciation", "depreciation"),
            ("Amortization", "amortization"), ("Net income", "net_income"),
            ("FCFE before dividends", "fcfe"), ("Cash and equivalents", "cash"))
    for label, dictionary in rows:
        print(f"{label}: {ns[dictionary][2030]:,.1f}")
    print("Operating profit (EBIT): " + f"{metric(result)['operating_profit']:,.1f}")


def main():
    print("AJG Lab 11: one-at-a-time sensitivity analysis")
    print("Run timestamp (UTC): " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"))
    print("Outputs are USD millions. Cash-flow label: FCFE before dividends.")
    print("Value per share: unavailable. The existing $100.82 formula discounts FCFE less dividends; reconcile that distribution convention before a per-share sensitivity or terminal value is used.\n")

    results = {}
    for label, shift in zip(CASES, (-GROWTH_SHIFT, 0.0, GROWTH_SHIFT)):
        results[("Revenue growth", label)] = fresh_model(growth_path(shift), BASE_COMP_TO_REVENUE)
    for label, shift in zip(CASES, (-COMP_SHIFT, 0.0, COMP_SHIFT)):
        results[("Compensation / revenue", label)] = fresh_model(BASE_GROWTH, BASE_COMP_TO_REVENUE + shift)

    original_base = results[("Revenue growth", "Base")]
    base_values = metric(original_base)
    for driver in ("Revenue growth", "Compensation / revenue"):
        print("\n" + driver)
        print("Case | Actual independent input | FY2030 operating profit | Change from base | FY2030 FCFE before dividends | Change from base | Accounting checks")
        valid = []
        for label in CASES:
            result = results[(driver, label)]
            values = metric(result)
            if values is None:
                print(f"{label} | {input_text(driver, result)} | INVALID | -- | INVALID | -- | {checks_text(result)}")
                continue
            valid.append(values)
            print(f"{label} | {input_text(driver, result)} | {values['operating_profit']:,.1f} | {signed(values['operating_profit'] - base_values['operating_profit'])} | {values['fcfe']:,.1f} | {signed(values['fcfe'] - base_values['fcfe'])} | {checks_text(result)}")
        if valid:
            op_span = max(row["operating_profit"] for row in valid) - min(row["operating_profit"] for row in valid)
            fcfe_span = max(row["fcfe"] for row in valid) - min(row["fcfe"] for row in valid)
            print(f"Output span (max - min across valid lower/base/higher): operating profit {op_span:,.1f}; FCFE {fcfe_span:,.1f}.")
        print_trace(driver, results[(driver, "Higher")])

    restored_base = fresh_model(BASE_GROWTH, BASE_COMP_TO_REVENUE)
    restored_values = metric(restored_base)
    restored = (restored_base["input_growth"] == original_base["input_growth"]
                and restored_base["input_comp"] == original_base["input_comp"]
                and restored_values == base_values and restored_base["checks"] == original_base["checks"])
    print("\nRestored-base check")
    print(f"Fresh base inputs, outputs, and accounting checks match the first base run exactly: {restored}.")
    print(f"FY2030E operating profit: {restored_values['operating_profit']:,.1f}; FY2030E FCFE before dividends: {restored_values['fcfe']:,.1f}.")
    print("Accounting checks: " + checks_text(restored_base))


if __name__ == "__main__":
    main()
