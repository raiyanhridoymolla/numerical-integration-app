"""
utils/tabular.py
Handles processing and validation of tabular x and y data.
"""

import numpy as np

def parse_table_input(x_str: str, y_str: str):
    """
    Parses comma-separated or space-separated string inputs for x and y into float lists.
    """
    try:
        x_vals = [float(v.strip()) for v in x_str.replace(',', ' ').split() if v.strip()]
        y_vals = [float(v.strip()) for v in y_str.replace(',', ' ').split() if v.strip()]
    except ValueError:
        raise ValueError("Inputs must contain only valid numbers.")

    if len(x_vals) != len(y_vals):
        raise ValueError(f"Count mismatch: {len(x_vals)} x-values and {len(y_vals)} f(x)-values provided.")

    if len(x_vals) < 2:
        raise ValueError("At least 2 data points are required.")

    return x_vals, y_vals


def validate_equally_spaced(x_vals, tol=1e-5):
    """
    Ensures x values are equally spaced and calculates step size h.
    """
    diffs = np.diff(x_vals)
    if not np.allclose(diffs, diffs[0], atol=tol):
        raise ValueError("x-values must be equally spaced for numerical integration rules.")
    return float(diffs[0])