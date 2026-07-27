# 📐 Numerical Integration Solver (Streamlit App)

A Streamlit web app that computes definite integrals using four numerical
integration methods, automatically selecting which methods are valid based
on the number of intervals `n`:

| Method              | Condition on n         |
|----------------------|-------------------------|
| Trapezoidal Rule      | any `n`                |
| Simpson's 1/3rd Rule  | `n` divisible by 2      |
| Simpson's 3/8th Rule  | `n` divisible by 3      |
| Weddle's Rule         | `n` divisible by 6      |

## Features
- **Two input modes**: analytical function `f(x)` or tabular `(x, y)` data
- Automatic rule applicability checking with clear warnings for skipped rules
- Step-by-step breakdown for every applicable method
- Comparison against the exact integral (via SymPy) with absolute/relative error
- Graphs: shaded area under the curve + bar chart comparing all methods
- CSV export of results
- Built-in example buttons for quick testing

## Project Structure
```
numerical_integration_app/
├── app.py                 # Main Streamlit app
├── requirements.txt
├── README.md
└── utils/
    ├── __init__.py
    ├── analytical.py       # f(x) parsing, sampling, exact integral
    ├── tabular.py           # table parsing & equal-spacing validation
    ├── rules.py             # Trapezoidal / Simpson's / Weddle's algorithms
    └── plotting.py          # matplotlib visualizations
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Deploy for Free (Streamlit Community Cloud)

1. Push this folder to a public GitHub repository.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app**, select your repo/branch, and set the main file path to `app.py`.
4. Click **Deploy** — you'll get a public URL you can share/present.

## Example Inputs

**Analytical function:**
```
f(x) = 1/(1+x**2)
a = 0, b = 6, n = 6
```

**Tabular data:**
```
x: 0, 1, 2, 3, 4, 5, 6
y: 1, 2, 5, 10, 17, 26, 37
```
