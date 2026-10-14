# Seaborn Tips — Distribution Visualizations

Three plots comparing restaurant tips across days, sex and lunch/dinner periods.

**Stack:** Python, pandas, seaborn, Matplotlib

## Covered plots

- Histogram with `hue='day'` and `element='step'`.
- `displot` with `hue='sex'`, `multiple='dodge'` and `palette='Set1'`.
- ECDF distribution with `hue='time'`, summer color palette and thicker lines.

The included public Tips CSV supports execution without Seaborn's example-data download. This is primarily a plotting-skills exercise.

## How to get started

```bash
python -m pip install -r requirements.txt
python src/seaborn_tips.py
```

[Open notebook](notebooks/seaborn_tips.ipynb) · [Sample data](data/tips.csv)
