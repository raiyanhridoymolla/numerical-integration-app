"""
utils/rules.py
Step-by-Step Breakdown for Numerical Integration Methods
"""

def trapezoidal_rule(y, h, decimals=4):
    n = len(y) - 1
    y_r = [round(val, decimals) for val in y]
    
    gen_formula = r"\int f(x)dx = \frac{\Delta x}{2} \left[(f(x_0) + f(x_n)) + 2(f(x_1) + f(x_2) + \dots + f(x_{n-1}))\right]"
    exp_formula = f"\\int f(x)dx = \\frac{{\\Delta x}}{{2}} \\left[" + " + ".join([
        f"f(x_{{{i}}})" if i in (0, n) else f"2f(x_{{{i}}})" for i in range(n + 1)
    ]) + "\\right]"
    
    m1_evals = []
    m1_vals = []
    for i in range(n + 1):
        if i in (0, n):
            val = y_r[i]
            m1_evals.append(f"f(x_{{{i}}}) = {val}")
        else:
            val = round(2 * y_r[i], decimals)
            m1_evals.append(f"2f(x_{{{i}}}) = 2 \\cdot {y_r[i]} = {val}")
        m1_vals.append(val)
        
    m1_sum = round(sum(m1_vals), decimals)
    ans = round((h / 2.0) * m1_sum, decimals)
    m1_sum_expr = " + ".join([str(v) for v in m1_vals])

    mid_sum = round(sum(y_r[1:-1]), decimals) if n > 1 else 0
    two_mid = round(2 * mid_sum, decimals)
    ends_sum = round(y_r[0] + y_r[-1], decimals)

    bd = {
        "rule_name": "Trapezoidal Rule",
        "gen_formula": gen_formula,
        "exp_formula": exp_formula,
        "m1_evals": m1_evals,
        "m1_sum_expr": m1_sum_expr,
        "m1_sum": m1_sum,
        "m2_step1": f"\\frac{{{h}}}{{2}} \\left[ ({y_r[0]} + {y_r[-1]}) + 2 \\times ({' + '.join(map(str, y_r[1:-1]))}) \\right]" if n > 1 else f"\\frac{{{h}}}{{2}} [{y_r[0]} + {y_r[-1]}]",
        "m2_step2": f"\\frac{{{h}}}{{2}} \\left[ ({y_r[0]} + {y_r[-1]}) + 2 \\times ({mid_sum}) \\right]" if n > 1 else "",
        "m2_step3": f"\\frac{{{h}}}{{2}} \\left[ ({ends_sum}) + ({two_mid}) \\right]" if n > 1 else f"\\frac{{{h}}}{{2}} [{ends_sum}]",
        "h": h,
        "n": n
    }
    return ans, bd


def simpsons_one_third(y, h, decimals=4):
    n = len(y) - 1
    y_r = [round(val, decimals) for val in y]
    
    gen_formula = r"\int f(x)dx = \frac{\Delta x}{3} \left[ (f(x_0) + f(x_n)) + 4(f(x_1) + f(x_3) + \dots) + 2(f(x_2) + f(x_4) + \dots) \right]"
    exp_formula = f"\\int f(x)dx = \\frac{{\\Delta x}}{{3}} \\left[" + " + ".join([
        f"f(x_{{{i}}})" if i in (0, n) else (f"4f(x_{{{i}}})" if i % 2 == 1 else f"2f(x_{{{i}}})")
        for i in range(n + 1)
    ]) + "\\right]"
    
    m1_evals = []
    m1_vals = []
    for i in range(n + 1):
        if i in (0, n):
            val = y_r[i]
            m1_evals.append(f"f(x_{{{i}}}) = {val}")
        elif i % 2 == 1:
            val = round(4 * y_r[i], decimals)
            m1_evals.append(f"4f(x_{{{i}}}) = 4 \\cdot {y_r[i]} = {val}")
        else:
            val = round(2 * y_r[i], decimals)
            m1_evals.append(f"2f(x_{{{i}}}) = 2 \\cdot {y_r[i]} = {val}")
        m1_vals.append(val)
        
    m1_sum = round(sum(m1_vals), decimals)
    ans = round((h / 3.0) * m1_sum, decimals)
    m1_sum_expr = " + ".join([str(v) for v in m1_vals])

    odds = [y_r[i] for i in range(1, n, 2)]
    evens = [y_r[i] for i in range(2, n, 2)]
    
    odd_sum = round(sum(odds), decimals)
    even_sum = round(sum(evens), decimals)
    four_odd = round(4 * odd_sum, decimals)
    two_even = round(2 * even_sum, decimals)
    ends_sum = round(y_r[0] + y_r[-1], decimals)

    bd = {
        "rule_name": "Simpson's 1/3 Rule",
        "gen_formula": gen_formula,
        "exp_formula": exp_formula,
        "m1_evals": m1_evals,
        "m1_sum_expr": m1_sum_expr,
        "m1_sum": m1_sum,
        "m2_step1": f"\\frac{{{h}}}{{3}} \\left[ ({y_r[0]} + {y_r[-1]}) + 4 \\times ({' + '.join(map(str, odds))}) + 2 \\times ({' + '.join(map(str, evens)) if evens else '0'}) \\right]",
        "m2_step2": f"\\frac{{{h}}}{{3}} \\left[ ({y_r[0]} + {y_r[-1]}) + 4 \\times ({odd_sum}) + 2 \\times ({even_sum}) \\right]",
        "m2_step3": f"\\frac{{{h}}}{{3}} \\left[ ({ends_sum}) + ({four_odd}) + ({two_even}) \\right]",
        "h": h,
        "n": n
    }
    return ans, bd


def simpsons_three_eighth(y, h, decimals=4):
    n = len(y) - 1
    y_r = [round(val, decimals) for val in y]
    
    gen_formula = r"\int f(x)dx = \frac{3\Delta x}{8} \left[ (f(x_0) + f(x_n)) + 2(f(x_3) + f(x_6) + \dots) + 3(f(x_1) + f(x_2) + f(x_4) + \dots) \right]"
    
    terms = []
    for i in range(n + 1):
        if i in (0, n):
            terms.append(f"f(x_{{{i}}})")
        elif i % 3 == 0:
            terms.append(f"2f(x_{{{i}}})")
        else:
            terms.append(f"3f(x_{{{i}}})")
    exp_formula = f"\\int f(x)dx = \\frac{{3\\Delta x}}{{8}} \\left[ " + " + ".join(terms) + " \\right]"

    m1_evals = []
    m1_vals = []
    for i in range(n + 1):
        if i in (0, n):
            val = y_r[i]
            m1_evals.append(f"f(x_{{{i}}}) = {val}")
        elif i % 3 == 0:
            val = round(2 * y_r[i], decimals)
            m1_evals.append(f"2f(x_{{{i}}}) = 2 \\cdot {y_r[i]} = {val}")
        else:
            val = round(3 * y_r[i], decimals)
            m1_evals.append(f"3f(x_{{{i}}}) = 3 \\cdot {y_r[i]} = {val}")
        m1_vals.append(val)

    m1_sum = round(sum(m1_vals), decimals)
    ans = round((3 * h / 8.0) * m1_sum, decimals)
    m1_sum_expr = " + ".join([str(v) for v in m1_vals])

    mult3 = [y_r[i] for i in range(1, n) if i % 3 == 0]
    others = [y_r[i] for i in range(1, n) if i % 3 != 0]

    mult3_sum = round(sum(mult3), decimals)
    others_sum = round(sum(others), decimals)
    two_mult3 = round(2 * mult3_sum, decimals)
    three_others = round(3 * others_sum, decimals)
    ends_sum = round(y_r[0] + y_r[-1], decimals)

    bd = {
        "rule_name": "Simpson's 3/8 Rule",
        "gen_formula": gen_formula,
        "exp_formula": exp_formula,
        "m1_evals": m1_evals,
        "m1_sum_expr": m1_sum_expr,
        "m1_sum": m1_sum,
        "m2_step1": f"\\frac{{3 \\times {h}}}{{8}} \\left[ ({y_r[0]} + {y_r[-1]}) + 2 \\times ({' + '.join(map(str, mult3)) if mult3 else '0'}) + 3 \\times ({' + '.join(map(str, others))}) \\right]",
        "m2_step2": f"\\frac{{3 \\times {h}}}{{8}} \\left[ ({y_r[0]} + {y_r[-1]}) + 2 \\times ({mult3_sum}) + 3 \\times ({others_sum}) \\right]",
        "m2_step3": f"\\frac{{3 \\times {h}}}{{8}} \\left[ ({ends_sum}) + ({two_mult3}) + ({three_others}) \\right]",
        "h": h,
        "n": n
    }
    return ans, bd


def weddles_rule(y, h, decimals=4):
    n = len(y) - 1
    y_r = [round(val, decimals) for val in y]

    gen_formula = r"\int f(x)dx = \frac{3\Delta x}{10} \left[ (f(x_0) + 5f(x_1) + f(x_2) + 6f(x_3) + f(x_4) + 5f(x_5) + f(x_6)) + \dots \right]"

    coeffs = [1, 5, 1, 6, 1, 5, 2]
    pattern = []
    for i in range(n + 1):
        if i == n:
            pattern.append(1)
        else:
            pattern.append(coeffs[i % 6])

    exp_terms = []
    for i, c in enumerate(pattern):
        if c == 1:
            exp_terms.append(f"f(x_{{{i}}})")
        else:
            exp_terms.append(f"{c}f(x_{{{i}}})")

    exp_formula = f"\\int f(x)dx = \\frac{{3\\Delta x}}{{10}} \\left[ " + " + ".join(exp_terms) + " \\right]"

    m1_evals = []
    m1_vals = []
    for i, c in enumerate(pattern):
        val = round(c * y_r[i], decimals)
        if c == 1:
            m1_evals.append(f"f(x_{{{i}}}) = {val}")
        else:
            m1_evals.append(f"{c}f(x_{{{i}}}) = {c} \\cdot {y_r[i]} = {val}")
        m1_vals.append(val)

    m1_sum = round(sum(m1_vals), decimals)
    ans = round((3 * h / 10.0) * m1_sum, decimals)
    m1_sum_expr = " + ".join([str(v) for v in m1_vals])

    grp_str = " + ".join([f"{c} \\times {y_r[i]}" if c > 1 else f"{y_r[i]}" for i, c in enumerate(pattern)])

    bd = {
        "rule_name": "Weddle's Rule",
        "gen_formula": gen_formula,
        "exp_formula": exp_formula,
        "m1_evals": m1_evals,
        "m1_sum_expr": m1_sum_expr,
        "m1_sum": m1_sum,
        "m2_step1": f"\\frac{{3 \\times {h}}}{{10}} \\left[ ({grp_str}) \\right]",
        "m2_step2": f"\\frac{{3 \\times {h}}}{{10}} \\left[ {m1_sum} \\right]",
        "m2_step3": f"\\frac{{3 \\times {h}}}{{10}} \\left[ {m1_sum} \\right]",
        "h": h,
        "n": n
    }
    return ans, bd