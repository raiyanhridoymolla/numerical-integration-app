"""
utils/tabular.py

Handles the "Tabular x, y values" input mode:
    - Validates that x-values are equally spaced
    - Extracts h (step size) and n (number of intervals)
"""

from typing import List, Tuple
import numpy as np


def validate_equally_spaced(x_values: List[float], tol: float = 1e-6) -> float:
    """
    Check that x-values are equally spaced within a tolerance.

    Returns:
        h (the common step size)

    Raises:
        ValueError if spacing is not uniform.
    """
    x = np.array(x_values, dtype=float)
    if len(x) < 2:
        raise ValueError("Need at least 2 x-values to compute an integral.")

    diffs = np.diff(x)
    h = diffs[0]

    if not np.all(np.abs(diffs - h) < tol):
        raise ValueError(
            "x-values must be equally spaced for Trapezoidal / Simpson's / Weddle's rules. "
            f"Detected spacings: {diffs.tolist()}"
        )
    if h <= 0:
        raise ValueError("x-values must be strictly increasing.")

    return float(h)


def parse_table_input(x_str: str, y_str: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Parse comma-separated x and y strings into numpy arrays.

    Example:
        x_str = "0, 1, 2, 3, 4, 5, 6"
        y_str = "1, 2, 5, 10, 17, 26, 37"
    """
    try:
        x_values = np.array([float(v.strip()) for v in x_str.split(",") if v.strip() != ""])
        y_values = np.array([float(v.strip()) for v in y_str.split(",") if v.strip() != ""])
    except ValueError as e:
        raise ValueError(f"Could not parse table values — make sure they are comma-separated numbers: {e}")

    if len(x_values) != len(y_values):
        raise ValueError(
            f"x and y must have the same number of values (got {len(x_values)} x-values "
            f"and {len(y_values)} y-values)."
        )
    if len(x_values) < 3:
        raise ValueError("Please provide at least 3 points (2 intervals).")

    return x_values, y_values
