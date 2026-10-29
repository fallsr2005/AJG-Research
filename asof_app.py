"""Lab 17 FRED/ALFRED point-in-time interest-rate audit.

Run with: python -m streamlit run asof_app.py
"""

import csv
import io
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd
import streamlit as st


FRED_GRAPH = "https://fred.stlouisfed.org/graph/fredgraph.csv"
ALFRED_GRAPH = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Effective federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year fixed mortgage rate",
}


def valid_series_id(series_id):
    """Allow only the ordinary alphanumeric FRED identifiers used in URLs."""
    cleaned = series_id.strip().upper()
    if not cleaned or not cleaned.replace("_", "").isalnum():
        raise ValueError("Enter a FRED series ID using letters, numbers, or underscores.")
    return cleaned


@st.cache_data(ttl=3_600, show_spinner=False)
def download_today(series_id):
    """Download the FRED values as they read today, one request per series."""
    series_id = valid_series_id(series_id)
    return download_csv(FRED_GRAPH, {"id": series_id}, series_id)


@st.cache_data(ttl=3_600, show_spinner=False)
def download_as_known_on(series_id, vintage_date):
    """Download the ALFRED vintage visible on the supplied decision date."""
    series_id = valid_series_id(series_id)
    return download_csv(
        ALFRED_GRAPH,
        {"id": series_id, "vintage_date": vintage_date.isoformat()},
        series_id,
    )


def download_csv(base_url, parameters, series_id):
    """Fetch and parse a public FRED/ALFRED graph CSV, omitting '.' missing data."""
    url = f"{base_url}?{urlencode(parameters)}"
    try:
        # FRED's public graph downloads accept their ordinary CSV URLs directly.
        # A custom user-agent caused intermittent connection resets in this environment.
        with urlopen(url, timeout=60) as response:
            text = response.read().decode("utf-8-sig")
    except HTTPError as error:
        raise ValueError(f"{series_id}: FRED/ALFRED returned HTTP {error.code}.") from error
    except URLError as error:
        raise ValueError(f"{series_id}: could not reach FRED/ALFRED ({error.reason}).") from error

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "observation_date" not in reader.fieldnames:
        raise ValueError(f"{series_id}: the download did not have an observation_date column.")
    value_column = series_id if series_id in reader.fieldnames else reader.fieldnames[-1]
    observations = []
    for row in reader:
        raw_value = (row.get(value_column) or "").strip()
        if raw_value in {"", "."}:
            continue
        try:
            observations.append((date.fromisoformat(row["observation_date"]), float(raw_value)))
        except (ValueError, TypeError) as error:
            raise ValueError(f"{series_id}: invalid observation in downloaded CSV.") from error
    if not observations:
        raise ValueError(f"{series_id}: no numeric observations were returned.")
    return observations


def since_start(observations, start_date):
    return [(observed, value) for observed, value in observations if observed >= start_date]


def last_observation(observations):
    """Return the last dated observation or None when a date filter leaves none."""
    return max(observations, key=lambda observation: observation[0]) if observations else None


def audit_row(series_id, current, as_of):
    """Compare a vintage with today's data without treating missing dates as revisions."""
    latest_as_of = last_observation(as_of)
    latest_current = last_observation(current)
    if latest_as_of is None or latest_current is None:
        raise ValueError(f"{series_id}: no observations remain after the selected start date.")

    current_by_date = dict(current)
    as_of_by_date = dict(as_of)
    current_value_on_as_of_date = current_by_date.get(latest_as_of[0])
    later_values = sum(observed > latest_as_of[0] for observed, _ in current)
    revised_values = sum(
        1
        for observed, vintage_value in as_of_by_date.items()
        if observed in current_by_date and current_by_date[observed] != vintage_value
    )
    return {
        "id": series_id,
        "as_of_date": latest_as_of[0],
        "as_of_value": latest_as_of[1],
        "current_date": latest_current[0],
        "current_value": latest_current[1],
        "current_value_on_as_of_date": current_value_on_as_of_date,
        "later_values": later_values,
        "revised_values": revised_values,
    }


def format_observation(observed, value):
    return f"{observed.isoformat()} — {value:,.2f}"


def render_audit_table(rows):
    """Use a Markdown table so each FRED ID is an actual source link."""
    lines = [
        "| Series | Last date/value as known then | Today's value on that date | Last date/value today | Values added later | Revised same-date values |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        source = f"[{row['id']}](https://fred.stlouisfed.org/series/{row['id']})"
        same_date_value = (
            f"{row['current_value_on_as_of_date']:,.2f}"
            if row["current_value_on_as_of_date"] is not None
            else "not available today"
        )
        lines.append(
            f"| {source} | {format_observation(row['as_of_date'], row['as_of_value'])} | "
            f"{same_date_value} | {format_observation(row['current_date'], row['current_value'])} | "
            f"{row['later_values']} | {row['revised_values']} |"
        )
    st.markdown("\n".join(lines))


st.set_page_config(page_title="Point-in-time rate audit", layout="wide")
st.title("Point-in-time rate audit")
today_label = f"{date.today():%B} {date.today().day}, {date.today():%Y}"
st.caption(
    f"Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded {today_label}; "
    "built with AI help, a learning demonstration, not investment advice."
)

with st.sidebar:
    st.header("Series and decision date")
    selected = st.multiselect(
        "Interest-rate series",
        options=list(SERIES),
        default=list(SERIES),
        format_func=lambda series_id: f"{series_id} — {SERIES[series_id]}",
    )
    additional = st.text_input("Add another FRED series ID", placeholder="Example: PAYEMS")
    start_date = st.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.date_input("As known on", value=date.today())

if additional.strip():
    try:
        selected.append(valid_series_id(additional))
    except ValueError as error:
        st.sidebar.error(str(error))

selected = list(dict.fromkeys(selected))
if not selected:
    st.info("Select at least one series ID to begin the audit.")
    st.stop()
if start_date > as_known_on:
    st.error("The start date cannot be after the as-known-on date.")
    st.stop()

rows = []
for series_id in selected:
    try:
        with st.spinner(f"Downloading {series_id} from FRED and ALFRED..."):
            current = since_start(download_today(series_id), start_date)
            as_of = since_start(download_as_known_on(series_id, as_known_on), start_date)
        result = audit_row(series_id, current, as_of)
        rows.append(result)

        st.subheader(f"{series_id} — {SERIES.get(series_id, 'Additional FRED series')}")
        chart = pd.DataFrame(current, columns=["Date", "Value"]).set_index("Date")
        st.line_chart(chart, use_container_width=True)
        st.write(
            f"Last date in the data known on {as_known_on.isoformat()}: "
            f"**{format_observation(result['as_of_date'], result['as_of_value'])}**"
        )
    except ValueError as error:
        st.error(str(error))
    except Exception as error:  # Keep an unknown or temporarily unavailable ID from stopping others.
        st.error(f"{series_id}: unexpected download error: {error}")

if rows:
    st.subheader("As-of audit table")
    render_audit_table(rows)
    st.caption(
        "Values added later counts current observations dated after the vintage's last observation. "
        "Revised same-date values counts dates available in both downloads whose numeric values differ."
    )
