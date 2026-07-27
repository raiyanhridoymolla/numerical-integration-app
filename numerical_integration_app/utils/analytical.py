"""
utils/analytical.py

Handles the "Analytical Function f(x)" input mode:
    - Parses the user's function string using sympy
    - Samples y-values at n+1 equally spaced points between a and b
    - Computes the exact definite integral (when possible) for error comparison
"""

from typing import Callable, List, Tuple, Optional
import numpy as np
import sympy as sp


def parse_function(func_str: str):
    """
    Parse a string like 'x**3 + 6*x**2 - 15*x + 7' or '1/(1+x**2)'
    into a sympy expression and a fast numeric callable.

    Returns:
        (sympy_expr, numeric_func, x_symbol)
    """
    x = sp.symbols('x')
    # Allow common aliases
    transformations = sp.parsing.sympy_parser.standard_transformations + (
        sp.parsing.sympy_parser.implicit_multiplication_application,
    )
    try:
        expr = sp.parsing.sympy_parser.parse_expr(
            func_str, transformations=transformations, local_dict={"x": x}
        )
    except Exception as e:
        raise ValueError(f"Could not parse function '{func_str}': {e}")

    numeric_func = sp.lambdify(x, expr, modules=["numpy"])
    return expr, numeric_func, x


def sample_function(numeric_func: Callable, a: float, b: float, n: int) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Generate n+1 equally spaced x-values between a and b and evaluate f(x).

    Returns:
        (x_values, y_values, h)
    """
    if n <= 0:
        raise ValueError("Number of intervals n must be a positive integer.")

    x_values = np.linspace(a, b, n + 1)
    h = (b - a) / n

    try:
        y_values = numeric_func(x_values)
        y_values = np.array(y_values, dtype=float)
        if y_values.shape == ():  # constant function edge case
            y_values = np.full_like(x_values, float(y_values))
    except Exception as e:
        raise ValueError(f"Error evaluating function over [{a}, {b}]: {e}")

    if np.any(np.isnan(y_values)) or np.any(np.isinf(y_values)):
        raise ValueError("Function produced NaN/Inf values in the given interval "
                          "(check for division by zero or domain issues).")

    return x_values, y_values, h


def exact_integral(expr, x_symbol, a: float, b: float) -> Optional[float]:
    """
    Attempt to compute the exact definite integral symbolically.
    Returns None if sympy cannot find a closed form or evaluation fails.
    """
    try:
        result = sp.integrate(expr, (x_symbol, a, b))
        value = float(result.evalf())
        if np.isnan(value) or np.isinf(value):
            return None
        return value
    except Exception:
        return None


def get_derivative_strings(expr, x_symbol) -> Tuple[str, str]:
    """Return f'(x) and f''(x) as readable strings (useful for display)."""
    f_prime = sp.diff(expr, x_symbol)
    f_double_prime = sp.diff(expr, x_symbol, 2)
    return str(sp.simplify(f_prime)), str(sp.simplify(f_double_prime))
