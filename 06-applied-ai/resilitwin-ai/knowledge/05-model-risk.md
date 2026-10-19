# Forecast model risk and evaluation
Source: Synthetic model governance memo / DEMO-OPS-05

Demand forecasts use a chronological validation holdout, and lagged features reference earlier dates only. A one-step-ahead holdout with observed lagged demand is not equivalent to a fully recursive multi-week forecast. Quantile residual bands shown in the dashboard are illustrative, not statistically calibrated future confidence intervals. Synthetic training data cannot establish production accuracy.
