"""Price three Meridian baselines using editable annual training assumptions."""

import csv
import io
from datetime import date
from math import isfinite, sqrt
from statistics import mean, stdev

# Rates and weights are decimals: 0.035 means 3.5%.
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160},
}
# Rows and columns follow the sleeve order above.
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
OBJECTIVE_RETURN = 0.065  # 2.5% estimated CPI + 4%; annual, before costs
RESERVE_SLEEVES = {"Treasury bills", "Treasury 10-year note"}


def validate_correlations(correlations, count):
    """Reject malformed, out-of-range, or asymmetric correlation tables."""
    if len(correlations) != count or any(len(row) != count for row in correlations):
        raise ValueError("Correlation table must have one row and column per sleeve.")
    for i, row in enumerate(correlations):
        for j, value in enumerate(row):
            if not isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation at row {i + 1}, column {j + 1} must be between -1 and 1.")
            if abs(value - correlations[j][i]) > 1e-12:
                raise ValueError("Correlation table must be symmetric.")
        if abs(row[i] - 1) > 1e-12:
            raise ValueError("Each diagonal correlation must equal 1.")


def covariance_matrix(sleeves, correlations):
    """Convert correlation and sleeve volatilities into covariance."""
    vols = [item["volatility"] for item in sleeves.values()]
    validate_correlations(correlations, len(vols))
    if any(not isfinite(vol) or vol <= 0 for vol in vols):
        raise ValueError("Sleeve volatilities must be positive and finite.")
    return [[correlations[i][j] * vols[i] * vols[j]
             for j in range(len(vols))] for i in range(len(vols))]


def baseline_weights(sleeves):
    """Return three named portfolios in the same order as sleeves."""
    names = list(sleeves)
    benchmark = {name: 0.0 for name in names}
    benchmark["Investment-grade bond fund"] = 0.4
    benchmark["Global equity index fund"] = 0.6
    inverse = {name: 1 / data["volatility"] for name, data in sleeves.items()}
    inverse_total = sum(inverse.values())
    return {
        "Benchmark": benchmark,
        "Equal weight": {name: 1 / len(names) for name in names},
        "Inverse volatility": {name: value / inverse_total for name, value in inverse.items()},
    }


def expected_return(weights, sleeves):
    return sum(weights[name] * data["return"] for name, data in sleeves.items())


def portfolio_volatility(weights, sleeves, covariance):
    """Square root of w' covariance w, including both cross-asset terms."""
    w = [weights[name] for name in sleeves]
    variance = sum(w[i] * w[j] * covariance[i][j]
                   for i in range(len(w)) for j in range(len(w)))
    if variance < -1e-12:
        raise ValueError("Portfolio variance is negative; check the correlation assumptions.")
    return sqrt(max(variance, 0.0))


def reserve_weight(weights, reserve_sleeves):
    return sum(weight for name, weight in weights.items() if name in reserve_sleeves)


def meets_objective(portfolio_return, objective):
    return portfolio_return >= objective


def search_portfolio(sleeves, correlations, objective, reserve_sleeves, minimum_reserve):
    """Search all 5-percentage-point long-only portfolios; return None if infeasible."""
    if not 0 <= minimum_reserve <= 1:
        raise ValueError("Reserve minimum must be between 0% and 100%.")
    names = list(sleeves)
    if not names:
        raise ValueError("At least one asset is required.")
    covariance = covariance_matrix(sleeves, correlations)
    best = None

    def compositions(total, count):
        if count == 1:
            yield (total,)
        else:
            for part in range(total + 1):
                for rest in compositions(total - part, count - 1):
                    yield (part,) + rest

    for units in compositions(20, len(names)):
        weights = {name: unit / 20 for name, unit in zip(names, units)}
        result = expected_return(weights, sleeves)
        reserve = reserve_weight(weights, reserve_sleeves)
        if result + 1e-12 < objective or reserve + 1e-12 < minimum_reserve:
            continue
        volatility = portfolio_volatility(weights, sleeves, covariance)
        if best is None or volatility < best["volatility"] - 1e-12:
            best = {"weights": weights, "return": result,
                    "volatility": volatility, "reserve": reserve}
    return best


def estimate_from_csv(source, last_36=False):
    """Annualize monthly simple returns; last_36 uses 36 returns and 37 prices."""
    raw = source.read() if hasattr(source, "read") else source
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(raw))
    rows = list(reader)
    if not rows or len(rows[0]) < 2 or rows[0][0].strip().lower() != "date":
        raise ValueError("CSV must start with a date column followed by ticker columns.")
    names = [name.strip() for name in rows[0][1:]]
    if not 3 <= len(names) <= 6 or any(not n for n in names) or len(set(names)) != len(names):
        raise ValueError("CSV must have 3 to 6 unique, nonempty ticker columns.")
    dates, prices = [], []
    for row in rows[1:]:
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != len(names) + 1:
            raise ValueError("Each CSV row must contain a date and one price per ticker.")
        try:
            day = date.fromisoformat(row[0].strip())
            values = [float(value) for value in row[1:]]
        except ValueError as exc:
            raise ValueError("Dates must be YYYY-MM-DD and prices must be numeric.") from exc
        if any(not isfinite(value) or value <= 0 for value in values):
            raise ValueError("Prices must be positive and finite.")
        if dates and (day.year * 12 + day.month != dates[-1].year * 12 + dates[-1].month + 1):
            raise ValueError("Prices must be in consecutive months, oldest first.")
        dates.append(day)
        prices.append(values)
    if len(prices) < 3:
        raise ValueError("At least three monthly prices are needed.")
    returns = [[prices[i][j] / prices[i - 1][j] - 1
                for i in range(1, len(prices))] for j in range(len(names))]
    if last_36:
        if len(prices) < 37:
            raise ValueError("The last 36 months require at least 37 monthly prices.")
        returns = [series[-36:] for series in returns]
    averages = [mean(series) for series in returns]
    deviations = [stdev(series) for series in returns]
    if any(sd <= 0 for sd in deviations):
        raise ValueError("Each asset must have nonzero historical volatility.")
    correlations = []
    for i in range(len(names)):
        row = []
        for j in range(len(names)):
            if i == j:
                row.append(1.0)
            else:
                covariance = sum((a - averages[i]) * (b - averages[j])
                                 for a, b in zip(returns[i], returns[j])) / (len(returns[i]) - 1)
                row.append(max(-1.0, min(1.0, covariance / (deviations[i] * deviations[j]))))
        correlations.append(row)
    sleeves = {name: {"return": averages[i] * 12,
                      "volatility": deviations[i] * sqrt(12)}
               for i, name in enumerate(names)}
    return sleeves, correlations, len(returns[0])


def main():
    try:
        covariance = covariance_matrix(SLEEVES, CORRELATIONS)
        portfolios = baseline_weights(SLEEVES)
        for name, weights in portfolios.items():
            result = expected_return(weights, SLEEVES)
            print(f"\n{name}")
            for sleeve, weight in weights.items():
                print(f"  {sleeve}: {weight * 100:.1f}%")
            print(f"  Expected return: {result * 100:.2f}%")
            print(f"  Volatility: {portfolio_volatility(weights, SLEEVES, covariance) * 100:.2f}%")
            print(f"  Reserve-eligible: {reserve_weight(weights, RESERVE_SLEEVES) * 100:.1f}%")
            print(f"  Meets {OBJECTIVE_RETURN * 100:.1f}% objective: {'yes' if meets_objective(result, OBJECTIVE_RETURN) else 'no'}")
    except ValueError as error:
        raise SystemExit(f"Input error: {error}") from error


if __name__ == "__main__":
    main()
