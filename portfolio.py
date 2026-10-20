"""Price three Meridian baselines using editable annual training assumptions."""

from math import isfinite, sqrt

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
