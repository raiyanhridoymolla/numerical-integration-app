"""
utils/rules.py

Core numerical integration algorithms:
    - Trapezoidal Rule            (valid for any n)
    - Simpson's 1/3rd Rule        (valid when n is even)
    - Simpson's 3/8th Rule        (valid when n is divisible by 3)
    - Weddle's Rule               (valid when n is divisible by 6)

Each function takes equally spaced y-values (y0, y1, ..., yn) and the
step size h, and returns the integral estimate plus a breakdown dict
that the UI can use to show step-by-step working.
"""

from typing import List, Dict, Tuple
import numpy as np


def get_applicable_rules(n: int) -> Dict[str, bool]:
    """
    Determine which numerical integration rules are valid for a given
    number of intervals n.

    Args:
        n: number of intervals (NOT number of points; points = n + 1)

    Returns:
        dict mapping rule name -> True/False (applicable or not)
    """
    return {
        "Trapezoidal": True,                 # always valid
        "Simpson's 1/3rd": n % 2 == 0,
        "Simpson's 3/8th": n % 3 == 0,
        "Weddle's": n % 6 == 0,
    }


def trapezoidal_rule(y: List[float], h: float) -> Tuple[float, Dict]:
    """
    Trapezoidal Rule:
        I = (h/2) * [ (y0 + yn) + 2*(y1 + y2 + ... + y(n-1)) ]
    """
    y = np.array(y, dtype=float)
    ends = y[0] + y[-1]
    middle = y[1:-1].sum() if len(y) > 2 else 0.0
    result = (h / 2) * (ends + 2 * middle)

    breakdown = {
        "formula": "I = (h/2) * [(y0 + yn) + 2*(sum of middle terms)]",
        "h": h,
        "ends_sum (y0+yn)": ends,
        "middle_sum": middle,
        "result": result,
    }
    return result, breakdown


def simpsons_one_third(y: List[float], h: float) -> Tuple[float, Dict]:
    """
    Simpson's 1/3rd Rule (requires n even, i.e. odd number of points):
        I = (h/3) * [ (y0 + yn) + 4*(sum of odd-indexed y) + 2*(sum of even-indexed y, excluding y0, yn) ]
    """
    y = np.array(y, dtype=float)
    n = len(y) - 1
    if n % 2 != 0:
        raise ValueError("Simpson's 1/3rd Rule requires n (number of intervals) to be even.")

    ends = y[0] + y[-1]
    odd_sum = y[1:-1:2].sum()    # indices 1, 3, 5, ...
    even_sum = y[2:-1:2].sum()   # indices 2, 4, 6, ... (excluding last)

    result = (h / 3) * (ends + 4 * odd_sum + 2 * even_sum)

    breakdown = {
        "formula": "I = (h/3) * [(y0+yn) + 4*(odd-indexed sum) + 2*(even-indexed sum)]",
        "h": h,
        "ends_sum (y0+yn)": ends,
        "odd_indexed_sum (4x)": odd_sum,
        "even_indexed_sum (2x)": even_sum,
        "result": result,
    }
    return result, breakdown


def simpsons_three_eighth(y: List[float], h: float) -> Tuple[float, Dict]:
    """
    Simpson's 3/8th Rule (requires n divisible by 3):
        I = (3h/8) * [ (y0 + yn) + 3*(terms NOT at multiples of 3) + 2*(terms AT multiples of 3, excluding y0, yn) ]
    """
    y = np.array(y, dtype=float)
    n = len(y) - 1
    if n % 3 != 0:
        raise ValueError("Simpson's 3/8th Rule requires n (number of intervals) to be divisible by 3.")

    ends = y[0] + y[-1]
    mult3_sum = 0.0
    other_sum = 0.0
    for i in range(1, n):
        if i % 3 == 0:
            mult3_sum += y[i]
        else:
            other_sum += y[i]

    result = (3 * h / 8) * (ends + 3 * other_sum + 2 * mult3_sum)

    breakdown = {
        "formula": "I = (3h/8) * [(y0+yn) + 3*(non-multiples of 3) + 2*(multiples of 3)]",
        "h": h,
        "ends_sum (y0+yn)": ends,
        "non_multiples_of_3_sum (3x)": other_sum,
        "multiples_of_3_sum (2x)": mult3_sum,
        "result": result,
    }
    return result, breakdown


def weddles_rule(y: List[float], h: float) -> Tuple[float, Dict]:
    """
    Weddle's Rule (requires n divisible by 6):
        Applied in blocks of 6 intervals (7 points per block):
        I_block = (3h/10) * [y0 + 5y1 + y2 + 6y3 + y4 + 5y5 + y6]
        Total I = sum of all blocks.
    """
    y = np.array(y, dtype=float)
    n = len(y) - 1
    if n % 6 != 0:
        raise ValueError("Weddle's Rule requires n (number of intervals) to be divisible by 6.")

    weights = np.array([1, 5, 1, 6, 1, 5, 1])
    total = 0.0
    block_details = []

    for start in range(0, n, 6):
        block_y = y[start:start + 7]
        block_val = (3 * h / 10) * np.dot(weights, block_y)
        total += block_val
        block_details.append({
            "interval_indices": f"{start} to {start + 6}",
            "y_values": block_y.tolist(),
            "block_result": block_val,
        })

    breakdown = {
        "formula": "I = sum over blocks of 6: (3h/10)*[y0 + 5y1 + y2 + 6y3 + y4 + 5y5 + y6]",
        "h": h,
        "num_blocks": len(block_details),
        "blocks": block_details,
        "result": total,
    }
    return total, breakdown


def compute_all_methods(y: List[float], h: float) -> Dict[str, Dict]:
    """
    Run every applicable rule (based on n) and collect results.

    Returns:
        dict keyed by method name -> {"applicable": bool, "reason": str,
                                       "result": float or None, "breakdown": dict or None}
    """
    n = len(y) - 1
    applicable = get_applicable_rules(n)
    results = {}

    rule_funcs = {
        "Trapezoidal": (trapezoidal_rule, "valid for any n"),
        "Simpson's 1/3rd": (simpsons_one_third, "requires n divisible by 2"),
        "Simpson's 3/8th": (simpsons_three_eighth, "requires n divisible by 3"),
        "Weddle's": (weddles_rule, "requires n divisible by 6"),
    }

    for name, (func, requirement) in rule_funcs.items():
        if applicable[name]:
            result, breakdown = func(y, h)
            results[name] = {
                "applicable": True,
                "reason": requirement,
                "result": result,
                "breakdown": breakdown,
            }
        else:
            results[name] = {
                "applicable": False,
                "reason": f"Skipped — {requirement} (n = {n})",
                "result": None,
                "breakdown": None,
            }

    return results
