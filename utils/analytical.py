"""
utils/analytical.py
Handles string formula parsing and function evaluation using SymPy.
"""

import sympy as sp

def parse_function(func_str: str):
    """
    Parses a math function string into a callable Python function.
    Supports inputs like '1 / (1 + x**2)', 'x^3 + 6*x^2 - 15*x + 7', 'sin(x)', 'exp(x)'
    """
    cleaned_str = func_str.replace('^', '**').strip()
    x = sp.Symbol('x')
    
    try:
        expr = sp.sympify(cleaned_str)
        numeric_func = sp.lambdify(x, expr, modules=['numpy', 'math'])
        return expr, numeric_func, x
    except Exception as e:
        raise ValueError(f"Invalid mathematical function: {e}")