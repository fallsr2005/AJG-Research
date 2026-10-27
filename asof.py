"""Lab 16: filter a small index table to what was knowable on a decision date.

All dates are publication dates or labeled monthly observations.  This is a
training example, so the records below are editable course-provided inputs.
"""

from datetime import date


DECISION_DATE = date.fromisoformat("2026-03-31")

# row, ticker, month measured, published on, index
ROWS = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def make_records(rows):
    """Parse editable rows into dictionaries with real date objects."""
    records = []
    for row_number, ticker, month, published, index in rows:
        records.append(
            {
                "row": row_number,
                "ticker": ticker,
                "month": month,
                "published": date.fromisoformat(published),
                "index": float(index),
            }
        )
    return records


def remove_no_ticker(records):
    """Rule 1: quarantine observations that cannot be assigned to a ticker."""
    kept = [record for record in records if record["ticker"]]
    removed = [record for record in records if not record["ticker"]]
    return kept, removed


def remove_exact_duplicates(records):
    """Rule 2: retain the first copy of a fully identical observation."""
    kept = []
    removed = []
    seen = set()
    for record in records:
        identity = (
            record["ticker"],
            record["month"],
            record["published"],
            record["index"],
        )
        if identity in seen:
            removed.append(record)
        else:
            seen.add(identity)
            kept.append(record)
    return kept, removed


def remove_after_decision_date(records, decision_date):
    """Rule 3: remove information that had not yet been published."""
    kept = [record for record in records if record["published"] <= decision_date]
    removed = [record for record in records if record["published"] > decision_date]
    return kept, removed


def keep_latest_vintage(records):
    """Rule 4: keep the most recently published vintage per ticker and month."""
    latest = {}
    for record in records:
        key = (record["ticker"], record["month"])
        # The row number breaks an otherwise exact publication-date tie predictably.
        if key not in latest or (record["published"], record["row"]) > (
            latest[key]["published"],
            latest[key]["row"],
        ):
            latest[key] = record
    kept = [record for record in records if latest[(record["ticker"], record["month"])] is record]
    removed = [record for record in records if record not in kept]
    return kept, removed


def asof_filter(records, decision_date):
    """Apply the required four point-in-time rules and retain the funnel."""
    panel, quarantined = remove_no_ticker(records)
    panel, duplicates = remove_exact_duplicates(panel)
    panel, after_date = remove_after_decision_date(panel, decision_date)
    panel, older_vintages = keep_latest_vintage(panel)
    funnel = [
        ("Quarantined: no ticker", quarantined),
        ("Exact duplicate", duplicates),
        (f"Published after {decision_date.isoformat()}", after_date),
        ("Older vintage replaced by a revision", older_vintages),
    ]
    return panel, funnel


def latest_month_signals(records):
    """Return each ticker's change from its previous available month to its latest."""
    by_ticker = {}
    for record in records:
        by_ticker.setdefault(record["ticker"], []).append(record)

    signals = {}
    for ticker, ticker_records in sorted(by_ticker.items()):
        ordered = sorted(ticker_records, key=lambda record: record["month"])
        if len(ordered) < 2:
            signals[ticker] = None
            continue
        previous, latest = ordered[-2], ordered[-1]
        change = (latest["index"] / previous["index"] - 1) * 100
        signals[ticker] = {"month": latest["month"], "change": change}
    return signals


def naive_panel(records):
    """Use all publications, then keep each ticker-month's latest vintage.

    This deliberately ignores whether the publication was available on the
    decision date.  It is the look-ahead-biased comparison, not a tradeable
    panel.
    """
    usable, _ = remove_no_ticker(records)
    usable, _ = remove_exact_duplicates(usable)
    panel, _ = keep_latest_vintage(usable)
    return panel


def row_numbers(records):
    """Format original input row identifiers for the funnel."""
    return ", ".join(str(record["row"]) for record in records) or "none"


def print_panel(panel):
    print("\nAs-of panel")
    print("Row  Ticker  Month measured  Published on  Index")
    for record in panel:
        print(
            f"{record['row']:>3}  {record['ticker']:<6}  {record['month']:<14}  "
            f"{record['published'].isoformat():<12}  {record['index']:.1f}"
        )


def print_signals(title, signals):
    print(f"\n{title}")
    for ticker, signal in signals.items():
        if signal is None:
            print(f"{ticker}: unavailable (fewer than two monthly observations)")
        else:
            print(f"{ticker}: {signal['change']:+.2f}% ({signal['month']})")


def main():
    records = make_records(ROWS)
    panel, funnel = asof_filter(records, DECISION_DATE)

    print(f"Decision date: {DECISION_DATE.isoformat()}")
    print("\nRow funnel")
    for label, removed in funnel:
        print(f"{label}: removed {len(removed)} row(s): {row_numbers(removed)}")

    print_panel(panel)
    print_signals("As-of signals", latest_month_signals(panel))
    print_signals(
        "Naive signals (latest publications, ignoring publication date)",
        latest_month_signals(naive_panel(records)),
    )


if __name__ == "__main__":
    main()
