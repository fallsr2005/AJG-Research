"""Comparable-company P/E calculator for FIN 43900 Lab 08.

All values below are editable. Prices and annual diluted EPS are per share in USD.
This program uses only the Python standard library and does not fetch data.
"""

import sys
from decimal import Decimal, InvalidOperation


# Comparison date: September 3, 2026.
# Prices: Nasdaq historical Close/Last for the same trading date.
# EPS: FY2025 total reported GAAP diluted EPS, not adjusted EPS.
TARGET = {
    "ticker": "AJG",
    "name": "Arthur J. Gallagher & Co.",
    "price": "266.66",
    "eps": "5.74",
}

PEERS = [
    {
        "ticker": "AON",
        "name": "Aon plc",
        "price": "327.00",
        "eps": "17.02",
    },
    {
        "ticker": "MRSH",
        "name": "Marsh (formerly Marsh McLennan)",
        "price": "188.46",
        "eps": "8.43",
    },
]

# Frozen Lab 07 training-case fixture. Run ``python comparable_policy.py
# --verify-lab07`` to confirm that later edits still reproduce the documented
# $215.81-$246.18 range, $231.00 median, and -$15.18 leave-one-out result.
LAB07_TARGET = {
    "ticker": "ABG",
    "name": "Asbury Automotive Group",
    "price": "243.03",
    "eps": "21.50",
}

LAB07_PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": "169.84", "eps": "16.92"},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": "421.48", "eps": "36.81"},
]


def as_decimal(value):
    """Return a finite Decimal, or None when a supplied input is unusable."""
    if value is None or isinstance(value, bool):
        return None
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    return number if number.is_finite() else None


def ticker_of(company):
    return str(company.get("ticker", "")).strip().upper()


def label_of(company):
    ticker = ticker_of(company)
    name = str(company.get("name", "")).strip()
    return f"{name} ({ticker})" if name and ticker else (name or ticker or "Unnamed company")


def format_money(value):
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"


def format_multiple(value):
    return f"{value:.6f}x"


def median(values):
    """Return the median without converting Decimal inputs to binary floats."""
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / Decimal("2")


def valid_company_values(company):
    """Return price, EPS, and a reason if P/E cannot be calculated."""
    price = as_decimal(company.get("price"))
    eps = as_decimal(company.get("eps"))
    if price is None or eps is None:
        return price, eps, "missing or nonnumeric price or EPS"
    if price <= 0:
        return price, eps, "nonpositive price"
    if eps <= 0:
        return price, eps, "nonpositive EPS"
    return price, eps, None


def collect_peers(target, peers):
    """Deduplicate peers, exclude the target, and retain only meaningful P/E inputs."""
    target_ticker = ticker_of(target)
    seen = set()
    valid = []
    notices = []

    for peer in peers:
        ticker = ticker_of(peer)
        peer_label = label_of(peer)
        if not ticker:
            notices.append(f"{peer_label}: excluded - missing ticker.")
            continue
        if ticker == target_ticker:
            notices.append(f"{peer_label}: excluded - target cannot be its own peer.")
            continue
        if ticker in seen:
            notices.append(f"{peer_label}: excluded - duplicate ticker.")
            continue
        seen.add(ticker)

        price, eps, reason = valid_company_values(peer)
        if reason:
            notices.append(f"{peer_label}: P/E not meaningful - {reason}.")
            continue
        valid.append({"company": peer, "price": price, "eps": eps, "pe": price / eps})

    return valid, notices


def print_leave_one_out(valid_peers, target_eps, full_median_price):
    print("\nLeave-one-out sensitivity (unrounded values used):")
    for removed in valid_peers:
        remaining = [peer for peer in valid_peers if peer is not removed]
        removed_label = label_of(removed["company"])
        if not remaining:
            print(f"  Remove {removed_label}: no estimate; no valid peers remain.")
            continue
        remaining_median = median([peer["pe"] for peer in remaining])
        remaining_price = remaining_median * target_eps
        change = remaining_price - full_median_price
        print(
            f"  Remove {removed_label}: remaining median-implied price "
            f"{format_money(remaining_price)}; change from full-peer median "
            f"{format_money(change)}."
        )


def verify_lab07_regression():
    """Check the saved Lab 07 training case without changing Lab 08 inputs."""
    target_price, target_eps, target_reason = valid_company_values(LAB07_TARGET)
    if target_reason:
        raise AssertionError(f"Lab 07 target inputs are invalid: {target_reason}")

    valid_peers, notices = collect_peers(LAB07_TARGET, LAB07_PEERS)
    if notices or len(valid_peers) != 2:
        raise AssertionError(f"Lab 07 peer fixture is invalid: {notices}")

    peer_multiples = [peer["pe"] for peer in valid_peers]
    median_multiple = median(peer_multiples)
    low_price = min(peer_multiples) * target_eps
    high_price = max(peer_multiples) * target_eps
    median_price = median_multiple * target_eps
    an = next(peer for peer in valid_peers if ticker_of(peer["company"]) == "AN")
    an_price = an["pe"] * target_eps
    leave_one_out_change = an_price - median_price

    actual = {
        "AN P/E": format_multiple(valid_peers[0]["pe"]),
        "GPI P/E": format_multiple(valid_peers[1]["pe"]),
        "ABG observed P/E": format_multiple(target_price / target_eps),
        "Range": f"{format_money(low_price)} to {format_money(high_price)}",
        "Median": format_money(median_price),
        "Remove GPI": f"{format_money(an_price)}; {format_money(leave_one_out_change)}",
    }
    expected = {
        "AN P/E": "10.037825x",
        "GPI P/E": "11.450149x",
        "ABG observed P/E": "11.303721x",
        "Range": "$215.81 to $246.18",
        "Median": "$231.00",
        "Remove GPI": "$215.81; -$15.18",
    }
    if actual != expected:
        raise AssertionError(f"Lab 07 regression mismatch: {actual}")

    print("Lab 07 regression check passed.")
    for label, value in actual.items():
        print(f"  {label}: {value}")


def main():
    target_price = as_decimal(TARGET.get("price"))
    target_eps = as_decimal(TARGET.get("eps"))
    print("Comparable-company P/E calculator")
    print(f"Target: {label_of(TARGET)}")

    if target_eps is None:
        print("Target EPS is not meaningful: missing or nonnumeric EPS.")
        return
    if target_eps <= 0:
        print("Target EPS is not meaningful: nonpositive EPS.")
        return

    if target_price is None:
        print("Target observed P/E (comparison only): not meaningful - missing or nonnumeric price.")
    elif target_price <= 0:
        print("Target observed P/E (comparison only): not meaningful - nonpositive price.")
    else:
        print(
            f"Target observed P/E (comparison only): "
            f"{format_multiple(target_price / target_eps)}"
        )
    valid_peers, notices = collect_peers(TARGET, PEERS)

    if notices:
        print("\nInput checks:")
        for notice in notices:
            print(f"  {notice}")

    if not valid_peers:
        print("\nNo usable peers: no peer-implied estimate.")
        return

    print("\nIncluded peer P/E multiples:")
    for peer in valid_peers:
        print(
            f"  {label_of(peer['company'])}: "
            f"{format_money(peer['price'])} / {format_money(peer['eps'])} = "
            f"{format_multiple(peer['pe'])}"
        )

    peer_multiples = [peer["pe"] for peer in valid_peers]
    full_median_multiple = median(peer_multiples)
    full_median_price = full_median_multiple * target_eps

    if len(valid_peers) == 1:
        peer = valid_peers[0]
        print("\nOne valid peer: reference estimate only; no range.")
        print(f"  Reference implied price: {format_money(full_median_price)}")
    else:
        low_multiple = min(peer_multiples)
        high_multiple = max(peer_multiples)
        low_price = low_multiple * target_eps
        high_price = high_multiple * target_eps
        print("\nPeer-implied valuation:")
        print(f"  Minimum peer P/E: {format_multiple(low_multiple)}")
        print(f"  Median peer P/E: {format_multiple(full_median_multiple)}")
        print(f"  Maximum peer P/E: {format_multiple(high_multiple)}")
        print(f"  Implied price range: {format_money(low_price)} to {format_money(high_price)}")
        print(f"  Median-implied price: {format_money(full_median_price)}")

    print_leave_one_out(valid_peers, target_eps, full_median_price)


if __name__ == "__main__":
    if "--verify-lab07" in sys.argv:
        verify_lab07_regression()
    else:
        main()
