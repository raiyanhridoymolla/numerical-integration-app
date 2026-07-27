"""
app.py

Streamlit web app for Numerical Integration using:
    - Trapezoidal Rule       (any n)
    - Simpson's 1/3rd Rule   (n divisible by 2)
    - Simpson's 3/8th Rule   (n divisible by 3)
    - Weddle's Rule          (n divisible by 6)

Supports two input modes:
    1. Analytical function f(x) over [a, b] with n intervals
    2. Tabular x, y data
"""

import streamlit as st
import pandas as pd
import numpy as np

from utils.analytical import (
    parse_function,
    sample_function,
    exact_integral,
    get_derivative_strings,
)
from utils.tabular import parse_table_input, validate_equally_spaced
from utils.rules import compute_all_methods, get_applicable_rules
from utils.plotting import plot_integration, plot_comparison_bar


# --------------------------------------------------------------------------
# Page config & custom CSS
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Numerical Integration Solver",
    page_icon="📐",
    layout="wide",
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1f4e79;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #555;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }
    .rule-card {
        background-color: #f0f4f8;
        border-left: 5px solid #1f77b4;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
    }
    .skipped-card {
        background-color: #fdf3f3;
        border-left: 5px solid #d62728;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
        color: #7a2727;
    }
    .stButton>button {
        background-color: #1f4e79;
        color: white;
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📐 Numerical Integration Solver</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Trapezoidal · Simpson\'s 1/3rd · Simpson\'s 3/8th · Weddle\'s Rule</div>',
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Sidebar: mode selection & example buttons
# --------------------------------------------------------------------------
st.sidebar.header("⚙️ Settings")
mode = st.sidebar.radio("Input Mode", ["Analytical Function f(x)", "Tabular Data (x, y)"])

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Quick Examples")

example_clicked = None
if mode == "Analytical Function f(x)":
    if st.sidebar.button("Example: 1/(1+x²), [0,6], n=6"):
        example_clicked = "func"
else:
    if st.sidebar.button("Example: Table (n=6)"):
        example_clicked = "table"

st.sidebar.markdown("---")
st.sidebar.caption(
    "Rule applicability:\n"
    "- Trapezoidal → any n\n"
    "- Simpson's 1/3rd → n divisible by 2\n"
    "- Simpson's 3/8th → n divisible by 3\n"
    "- Weddle's → n divisible by 6"
)

results = None
x_values = y_values = None
h = None
numeric_func = None
a = b = None
exact_val = None


# --------------------------------------------------------------------------
# MODE 1: Analytical Function
# --------------------------------------------------------------------------
if mode == "Analytical Function f(x)":
    st.subheader("Method 1 — Analytical Function")

    col1, col2, col3 = st.columns(3)
    default_func = "1/(1+x**2)" if example_clicked == "func" else "x**3 + 6*x**2 - 15*x + 7"
    default_a = 0.0 if example_clicked == "func" else 0.0
    default_b = 6.0 if example_clicked == "func" else 4.0
    default_n = 6 if example_clicked == "func" else 4

    with col1:
        func_str = st.text_input("f(x) =", value=default_func,
                                  help="Use Python syntax, e.g. x**2, 1/(1+x**2), sin(x)")
    with col2:
        a = st.number_input("Lower limit (a)", value=float(default_a))
        b = st.number_input("Upper limit (b)", value=float(default_b))
    with col3:
        n = st.number_input("Number of intervals (n)", min_value=1, value=int(default_n), step=1)

    if st.button("🔍 Compute Integral", key="compute_analytical"):
        try:
            expr, numeric_func, x_sym = parse_function(func_str)
            x_values, y_values, h = sample_function(numeric_func, a, b, int(n))
            exact_val = exact_integral(expr, x_sym, a, b)
            results = compute_all_methods(y_values.tolist(), h)

            f_prime_str, f_double_prime_str = get_derivative_strings(expr, x_sym)

            st.success("✅ Computation successful")
            st.markdown(f"**f(x) = {str(expr)}**")
            st.markdown(f"- f'(x) = `{f_prime_str}`")
            st.markdown(f"- f''(x) = `{f_double_prime_str}`")
            st.markdown(f"- Step size h = `{h:.6f}`  |  n = `{int(n)}`")

            st.markdown("**Sample points:**")
            sample_df = pd.DataFrame({"x": x_values, "f(x)": y_values})
            st.dataframe(sample_df.style.format({"x": "{:.4f}", "f(x)": "{:.6f}"}), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")


# --------------------------------------------------------------------------
# MODE 2: Tabular Data
# --------------------------------------------------------------------------
else:
    st.subheader("Method 2 — Tabular Data")

    default_x = "0, 1, 2, 3, 4, 5, 6" if example_clicked == "table" else "0, 1, 2, 3, 4"
    default_y = "1, 2, 5, 10, 17, 26, 37" if example_clicked == "table" else "1, 2, 5, 10, 17"

    col1, col2 = st.columns(2)
    with col1:
        x_str = st.text_area("x values (comma separated)", value=default_x, height=80)
    with col2:
        y_str = st.text_area("y values (comma separated)", value=default_y, height=80)

    if st.button("🔍 Compute Integral", key="compute_tabular"):
        try:
            x_values, y_values = parse_table_input(x_str, y_str)
            h = validate_equally_spaced(x_values)
            a, b = float(x_values[0]), float(x_values[-1])
            n = len(x_values) - 1

            results = compute_all_methods(y_values.tolist(), h)

            st.success("✅ Computation successful")
            st.markdown(f"- Detected step size h = `{h:.6f}`  |  n = `{n}`  |  interval = `[{a}, {b}]`")

            st.markdown("**Input Data:**")
            table_df = pd.DataFrame({"x": x_values, "y": y_values})
            st.dataframe(table_df.style.format({"x": "{:.4f}", "y": "{:.6f}"}), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")


# --------------------------------------------------------------------------
# Display Results (shared for both modes)
# --------------------------------------------------------------------------
if results is not None:
    st.markdown("---")
    st.subheader("📊 Applicable Rules & Results")

    n_used = len(y_values) - 1
    applicable = get_applicable_rules(n_used)

    summary_rows = []
    for method_name, res in results.items():
        if res["applicable"]:
            row = {"Method": method_name, "Result": res["result"]}
            if exact_val is not None:
                abs_err = abs(exact_val - res["result"])
                rel_err = (abs_err / abs(exact_val) * 100) if exact_val != 0 else float("nan")
                row["Exact Value"] = exact_val
                row["Absolute Error"] = abs_err
                row["Relative Error %"] = rel_err
            summary_rows.append(row)

            with st.expander(f"✅ {method_name} — Result = {res['result']:.6f}", expanded=False):
                st.markdown(f"**Formula:** `{res['breakdown']['formula']}`")
                for k, v in res["breakdown"].items():
                    if k in ("formula", "blocks"):
                        continue
                    st.write(f"- **{k}**: {v}")
                if "blocks" in res["breakdown"]:
                    st.write("**Block-wise breakdown (Weddle's):**")
                    st.dataframe(pd.DataFrame(res["breakdown"]["blocks"]), use_container_width=True)
        else:
            st.markdown(
                f'<div class="skipped-card">⚠️ <b>{method_name}</b> — {res["reason"]}</div>',
                unsafe_allow_html=True,
            )

    if summary_rows:
        st.markdown("### 📋 Comparison Table")
        summary_df = pd.DataFrame(summary_rows)
        st.dataframe(summary_df.style.format(precision=6), use_container_width=True)

        csv = summary_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Results as CSV",
            data=csv,
            file_name="numerical_integration_results.csv",
            mime="text/csv",
        )

        # --------------------------------------------------------------
        # Plots
        # --------------------------------------------------------------
        st.markdown("### 📈 Graphs")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig1 = plot_integration(
                x_values, y_values, a, b,
                numeric_func=numeric_func,
                method_name="Selected Interval",
            )
            st.pyplot(fig1)

        with col_g2:
            fig2 = plot_comparison_bar(results, exact_value=exact_val)
            st.pyplot(fig2)

st.markdown("---")
st.caption("Numerical Integration Solver · Trapezoidal, Simpson's 1/3rd, Simpson's 3/8th, Weddle's Rule")
