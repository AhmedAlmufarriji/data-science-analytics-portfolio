# Restaurant Tips — Exploratory Data Analysis

Explore the 244-record Tips dataset with six visualizations and twelve evidence-based observations.

**Stack:** Python, pandas, NumPy, seaborn, Matplotlib

## Analysis workflow

1. Read the included public sample dataset `src/tips.csv`.
2. **Univariate:** total-bill distribution and count of bills by day.
3. **Bivariate:** bill versus tip scatter/regression plot; tip distribution by day.
4. **Multivariate:** bill, tip, party size and meal period; mean tips split by day and sex.
5. Interpret patterns carefully: associations do not establish causation.

The example dataset is small and is intended for visualization practice, not for representative restaurant business forecasting.

## How to get started

```bash
python -m pip install -r requirements.txt
python src/eda_tips.py
```

[Open notebook](notebooks/eda_tips.ipynb) · [View sample data](data/tips.csv)
