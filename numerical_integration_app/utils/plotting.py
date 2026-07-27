"""
utils/plotting.py

Plotting helpers to visualize the function / data and the shaded area
representing the numerical integration estimate.
"""

from typing import Callable, Optional
import numpy as np
import matplotlib.pyplot as plt


def plot_integration(
    x_values: np.ndarray,
    y_values: np.ndarray,
    a: float,
    b: float,
    numeric_func: Optional[Callable] = None,
    method_name: str = "Numerical Integration",
):
    """
    Plot the function (smooth curve if numeric_func is provided, otherwise
    a straight-line interpolation through data points), shade the area
    under the curve between a and b, and mark the sample points used.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    if numeric_func is not None:
        x_smooth = np.linspace(a, b, 400)
        y_smooth = numeric_func(x_smooth)
        ax.plot(x_smooth, y_smooth, color="#1f77b4", linewidth=2, label="f(x)")
        ax.fill_between(x_smooth, y_smooth, color="#1f77b4", alpha=0.2)
    else:
        ax.plot(x_values, y_values, color="#1f77b4", linewidth=2, label="Data (linear interp.)")
        ax.fill_between(x_values, y_values, color="#1f77b4", alpha=0.2)

    ax.scatter(x_values, y_values, color="#d62728", zorder=5, label="Sample points", s=40)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Area under curve — {method_name}")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig


def plot_comparison_bar(results: dict, exact_value: Optional[float] = None):
    """
    Bar chart comparing the integral estimates from each applicable method,
    with a horizontal reference line for the exact value if available.
    """
    methods = [name for name, r in results.items() if r["applicable"]]
    values = [results[name]["result"] for name in methods]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(methods, values, color="#2ca02c", alpha=0.8)

    if exact_value is not None:
        ax.axhline(exact_value, color="red", linestyle="--", linewidth=1.5, label=f"Exact = {exact_value:.6f}")
        ax.legend()

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{val:.5f}", ha="center", va="bottom", fontsize=9)

    ax.set_ylabel("Integral Value")
    ax.set_title("Comparison of Numerical Integration Methods")
    plt.xticks(rotation=15)
    plt.tight_layout()

    return fig
