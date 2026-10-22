"""Interactive Lab 15 portfolio search; calculations live in portfolio.py."""
import hashlib
import importlib

import streamlit as st
import portfolio

# Reload so a saved change to the engine's training inputs appears on rerun.
portfolio = importlib.reload(portfolio)

st.set_page_config(page_title="Portfolio stability decision", layout="wide")
st.title("Portfolio stability decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Mandate and data")
    objective = st.number_input("Expected return objective (%)", value=6.5, step=0.1) / 100
    minimum = st.number_input("Minimum reserve weight (%)", min_value=0.0,
                              max_value=100.0, value=3.0, step=1.0) / 100
    upload = st.file_uploader("Monthly adjusted prices CSV", type="csv")
    last_36 = st.checkbox("Use the last 36 monthly returns")

try:
    if upload is None:
        loaded = portfolio.SLEEVES
        loaded_corr = portfolio.CORRELATIONS
        current_data, current_corr = loaded, loaded_corr
        default_reserve = portfolio.RESERVE_SLEEVES
        context = "meridian"
        if last_36:
            st.info("The 36-month option applies after a price CSV is uploaded.")
        st.write("Meridian: course-authored annual training assumptions.")
    else:
        raw = upload.getvalue()
        loaded, loaded_corr, all_count = portfolio.estimate_from_csv(raw)
        current_data, current_corr, current_count = portfolio.estimate_from_csv(raw, last_36)
        default_reserve = {"SGOV"} & set(current_data)
        context = hashlib.sha256(raw).hexdigest()[:12] + ("36" if last_36 else "all")
        st.write(f"Historical estimates, not forecasts. Current: {current_count} monthly returns; "
                 f"loaded comparison: all {all_count} monthly returns. Annualized mean = monthly "
                 "mean × 12; annualized sample volatility = monthly standard deviation × √12.")

    st.subheader("Editable return estimates and reserve eligibility")
    edited = {}
    selected_reserve = set()
    for name, data in current_data.items():
        a, b = st.columns([3, 2])
        with a:
            value = st.number_input(f"{name} expected return (%)", value=float(data["return"] * 100),
                                    step=0.1, format="%.4f", key=f"return_{context}_{name}") / 100
        with b:
            checked = st.checkbox(f"{name} reserve-eligible", value=name in default_reserve,
                                  key=f"reserve_{name}")
        if checked:
            selected_reserve.add(name)
        edited[name] = {"return": value, "volatility": data["volatility"]}

    current = portfolio.search_portfolio(edited, current_corr, objective, selected_reserve, minimum)
    reference = portfolio.search_portfolio(loaded, loaded_corr, objective, selected_reserve, minimum)

    def show_result(title, result):
        st.subheader(title)
        if result is None:
            st.warning("No mix meets the objective and reserve minimum on the 5-point grid.")
            return
        for name, weight in result["weights"].items():
            st.write(f"{name}: {weight * 100:.2f}%")
        st.write(f"Expected return: {result['return'] * 100:.2f}%")
        st.write(f"Volatility: {result['volatility'] * 100:.2f}%")
        st.write(f"Reserve-eligible: {result['reserve'] * 100:.2f}%")

    left, right = st.columns(2)
    with left:
        show_result("Current inputs", current)
    with right:
        show_result("Inputs as loaded (all months)", reference)
    if current is not None and reference is not None:
        change = max(abs(current["weights"][name] - reference["weights"][name])
                     for name in current["weights"]) * 100
        st.write(f"Largest weight change: {change:.2f} percentage points")
    else:
        st.write("Largest weight change: unavailable because at least one mix is infeasible.")
    st.caption("Search uses long-only weights in 5-percentage-point steps. Both comparisons use "
               "the current objective, reserve minimum, and reserve eligibility selections.")
except (ValueError, UnicodeError) as error:
    st.error(f"Input error: {error}")
