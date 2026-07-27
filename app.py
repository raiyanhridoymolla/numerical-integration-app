"""
app.py
Numerical Integration App matching exact reference interface and solution step layouts.
"""

import random
import numpy as np
import pandas as pd
import streamlit as st

from utils.analytical import parse_function
from utils.tabular import parse_table_input, validate_equally_spaced
from utils.rules import (
    trapezoidal_rule,
    simpsons_one_third,
    simpsons_three_eighth,
    weddles_rule,
)

# Page Config
st.set_page_config(
    page_title="Numerical Integration Solver",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1a1a1a; margin-bottom: 2px; }
    .sub-header { font-size: 0.95rem; color: #666666; margin-bottom: 25px; }
    .section-title { font-size: 1.6rem; font-weight: 600; color: #2c3e50; margin-top: 15px; }
    
    div.stButton > button[key="btn_find"] {
        background-color: #ff0000 !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        border: none !important;
    }
    div.stButton > button[key="btn_find"]:hover {
        background-color: #cc0000 !important;
    }
</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.markdown("## ⚙️ Settings")

st.sidebar.markdown("**Navigation**")
nav_choice = st.sidebar.radio("Nav", ["🔍 Calculator", "📄 View Source Code"], label_visibility="collapsed")

st.sidebar.markdown("**Choose Input Method**")
input_method = st.sidebar.radio("Input Method", ["Analytical Function f(x)", "Tabular Data (x, y)"], label_visibility="collapsed")

st.sidebar.markdown("**Select Integration Method**")
selected_rule = st.sidebar.selectbox("Integration Rule", ["Trapezoidal Rule", "Simpson's 1/3rd Rule", "Simpson's 3/8th Rule", "Weddle's Rule"], label_visibility="collapsed")

st.sidebar.markdown("**Decimal Places**")
decimals = st.sidebar.selectbox("Decimals", [2, 4, 6], index=1, label_visibility="collapsed")

st.sidebar.markdown("---")
with st.sidebar.expander("ℹ️ About", expanded=True):
    st.info("""
    **Numerical Integration Solver** computes integrals using Trapezoidal, Simpson's, and Weddle's Rules.
    """)

# MAIN CONTENT
if nav_choice == "📄 View Source Code":
    st.title("📄 Source Code")
    st.info("Check `app.py` and `utils/` folder for source logic.")

else:
    st.markdown('<div class="main-header">📈 Numerical Integration Solver</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Using Numerical Integration — Analytical & Tabular Methods</div>', unsafe_allow_html=True)

    if "func_val" not in st.session_state:
        st.session_state.func_val = "1 / (1 + x**2)"
    if "x_range_val" not in st.session_state:
        st.session_state.x_range_val = "0, 1, 2, 3, 4, 5, 6"
    if "table_val" not in st.session_state:
        st.session_state.table_val = "7.47, 7.48, 7.49, 7.50, 7.51, 7.52, 7.53\n1.93, 1.95, 1.98, 2.01, 2.03, 2.06, 2.09"

    x_vals = []
    y_vals = []
    find_pressed = False

    if input_method == "Analytical Function f(x)":
        st.markdown(f"### Method — {selected_rule} (Analytical Function)")
        st.markdown("**f(x) =**")
        col_in1, col_in2 = st.columns([3, 1])
        
        with col_in1:
            func_input = st.text_input("Function Input", value=st.session_state.func_val, label_visibility="collapsed")
        with col_in2:
            example = st.selectbox("-- pick example --", ["-- pick example --", "1 / (1 + x**2)", "x**3 + 6*x**2 - 15*x + 7", "sin(x)", "exp(x)"])
            if example != "-- pick example --":
                func_input = example

        st.markdown("**x values (comma separated) =**")
        x_range_str = st.text_input("x range", value=st.session_state.x_range_val, label_visibility="collapsed")

        btn_col1, btn_col2, _ = st.columns([1, 1, 4])
        with btn_col1:
            find_pressed = st.button("🔍 Find", key="btn_find", use_container_width=True)
        with btn_col2:
            random_pressed = st.button("🎲 Random", key="btn_rnd", use_container_width=True)

        if random_pressed:
            sample_funcs = ["x**2 + 2*x + 1", "1 / (1 + x)", "cos(x)", "x**3 - 3*x"]
            st.session_state.func_val = random.choice(sample_funcs)
            st.rerun()

        if find_pressed:
            try:
                expr, numeric_func, _ = parse_function(func_input)
                x_vals = [float(v.strip()) for v in x_range_str.split(",") if v.strip()]
                y_vals = [float(numeric_func(v)) for v in x_vals]
            except Exception as e:
                st.error(f"❌ Error in function parsing: {e}")

    else:
        st.markdown(f"### Method — {selected_rule} (Tabular Data)")
        st.markdown("**Type your data (x values on Line 1, f(x) values on Line 2):**")
        raw_table = st.text_area("Table Input", value=st.session_state.table_val, height=100)
        
        btn_col1, _ = st.columns([1, 5])
        with btn_col1:
            find_pressed = st.button("🔍 Find", key="btn_find", use_container_width=True)

        if find_pressed:
            lines = [l.strip() for l in raw_table.strip().split("\n") if l.strip()]
            if len(lines) >= 2:
                try:
                    x_vals, y_vals = parse_table_input(lines[0], lines[1])
                except Exception as e:
                    st.error(f"❌ Table input error: {e}")

    # SOLUTION DISPLAY
    if find_pressed and len(x_vals) > 1 and len(y_vals) == len(x_vals):
        try:
            h = validate_equally_spaced(x_vals)
            n = len(x_vals) - 1

            valid = True
            err_msg = ""
            if selected_rule == "Simpson's 1/3rd Rule" and n % 2 != 0:
                valid = False
                err_msg = f"Simpson's 1/3rd Rule requires n (intervals) to be even. Given n = {n}."
            elif selected_rule == "Simpson's 3/8th Rule" and n % 3 != 0:
                valid = False
                err_msg = f"Simpson's 3/8th Rule requires n to be divisible by 3. Given n = {n}."
            elif selected_rule == "Weddle's Rule" and n % 6 != 0:
                valid = False
                err_msg = f"Weddle's Rule requires n to be divisible by 6. Given n = {n}."

            if not valid:
                st.error(f"❌ {err_msg}")
            else:
                st.success("Solution found!")
                st.markdown("---")
                st.markdown('<div class="section-title">📝 Solution</div>', unsafe_allow_html=True)

                if selected_rule == "Trapezoidal Rule":
                    ans, bd = trapezoidal_rule(y_vals, h, decimals)
                elif selected_rule == "Simpson's 1/3rd Rule":
                    ans, bd = simpsons_one_third(y_vals, h, decimals)
                elif selected_rule == "Simpson's 3/8th Rule":
                    ans, bd = simpsons_three_eighth(y_vals, h, decimals)
                else:
                    ans, bd = weddles_rule(y_vals, h, decimals)

                # Step 1
                st.markdown("### Step-1: Value Table")
                st.write("Constructing table for $x$ and $f(x)$ values:")
                tbl_data = []
                for i in range(len(x_vals)):
                    tbl_data.append({
                        "x Index": f"x_{i}",
                        "x Value": round(x_vals[i], decimals),
                        "f(x) Value": round(y_vals[i], decimals)
                    })
                st.table(pd.DataFrame(tbl_data))
                st.write(f"Interval spacing $\\Delta x = h = {h}$ and intervals $n = {n}$.")

                st.markdown("---")

                # Step 2
                st.markdown("### Step-2: Apply Integration Formula (Method-1)")
                st.write(f"Formula for **{selected_rule}**:")
                st.latex(bd.get("gen_formula", r"\int f(x)dx"))
                st.latex(bd.get("exp_formula", ""))

                st.write("**Calculating individual terms:**")
                for eq in bd.get("m1_evals", []):
                    st.latex(eq)

                st.write("**Summing up evaluated terms:**")
                st.latex(f"\\int f(x)dx = \\text{{multiplier}} \\cdot ({bd.get('m1_sum_expr', '')})")
                st.latex(f"= \\text{{multiplier}} \\cdot ({bd.get('m1_sum', '')})")
                st.latex(f"= {ans}")

                st.markdown("---")

                # Step 3
                st.markdown("### Step-3: Grouped Solution (Method-2)")
                st.latex(bd.get("gen_formula", r"\int f(x)dx"))
                if bd.get("m2_step1"):
                    st.latex(f"= {bd['m2_step1']}")
                if bd.get("m2_step2"):
                    st.latex(f"= {bd['m2_step2']}")
                if bd.get("m2_step3"):
                    st.latex(f"= {bd['m2_step3']}")
                st.latex(f"= {ans}")

                st.markdown("---")

                # Step 4
                st.markdown("### Step-4: Final Result")
                st.info(f"**Solution by {selected_rule} is {ans}**")

        except Exception as e:
            st.error(f"❌ Error during calculation: {e}")