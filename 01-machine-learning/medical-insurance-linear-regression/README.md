# Medical Insurance Cost Prediction — Linear Regression

Estimate medical insurance charges using demographic and lifestyle features. This reproduces a course exercise rather than a validated underwriting tool.

**Stack:** Python, pandas, NumPy, seaborn, Matplotlib, scikit-learn

## Data and methodology

- **Data:** the public 1,338-row insurance.csv teaching dataset, available from [Kaggle](https://www.kaggle.com/datasets/mirichoi0218/insurance). Download it locally if the notebook cannot reach the public mirror.
- **Target:** `charges`. Features include age, sex, BMI, children, smoker and region.
- **EDA:** `head`, `info`, `describe`, charges histogram, feature pairplot and correlation heatmap.
- **Preprocessing:** LabelEncoder on the three categorical fields, following the course brief.
- **Training:** `LinearRegression` with 70% train / 30% test and `random_state=23`.
- **Evaluation:** MAE, MSE, RMSE and R² plus actual-versus-predicted and residual plots.

## Limitations

This baseline uses ordinal label encoding for region; one-hot encoding and cross-validation are better choices for a realistic predictive application. No causal conclusions or clinical decisions should be drawn from this dataset.

## How to get started

```bash
python -m pip install -r requirements.txt
python src/insurance_linear_regression.py --data insurance.csv
```

[Open the Jupyter notebook](notebooks/insurance_linear_regression.ipynb)
