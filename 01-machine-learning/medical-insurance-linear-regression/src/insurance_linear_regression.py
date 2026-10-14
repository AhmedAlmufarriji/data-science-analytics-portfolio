"""Medical insurance cost prediction: EDA and Linear Regression (70/30 split)."""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_URL = (
    "https://raw.githubusercontent.com/pplonski/datasets-for-start/"
    "refs/heads/master/insurance/insurance.csv"
)
CATEGORICAL = ("sex", "smoker", "region")
FEATURES = ("age", "sex", "bmi", "children", "smoker", "region")


def read_insurance_data(data_path="insurance.csv"):
    """Prefer the local Kaggle CSV; otherwise read the identical public GitHub mirror."""
    file = Path(data_path)
    try:
        df = pd.read_csv(file if file.is_file() else DATA_URL)
    except Exception as exc:
        raise RuntimeError(
            "Could not load insurance.csv. Download it from the provided Kaggle "
            "dataset and place it next to this script, then rerun."
        ) from exc
    required = set(FEATURES) | {"charges"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing required columns: {sorted(required - set(df.columns))}")
    if df[list(required)].isna().any().any():
        raise ValueError("Missing values found in required columns; handle them first.")
    return df


def generate_report(df, output_dir="results", draw_plots=True):
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    print("\nSTEP 1 - EXPLORATORY DATA ANALYSIS (EDA)")
    print("Dataset shape:", df.shape)
    print("\nHEAD:\n", df.head())
    print("\nINFO:")
    df.info()
    print("\nDESCRIBE:\n", df.describe(include="all"))
    print("\nMISSING VALUES:\n", df.isnull().sum())

    if draw_plots:
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(8.5, 5))
        sns.histplot(data=df, x="charges", bins=35, kde=True, color="#246a91", ax=ax)
        ax.set_title("Distribution of Medical Insurance Charges")
        ax.set(xlabel="Charges (USD)", ylabel="Count")
        fig.tight_layout()
        fig.savefig(folder / "01_charges_distribution.png", dpi=180)
        plt.close(fig)

        pair_columns = ["age", "bmi", "children", "charges", "smoker"]
        g = sns.pairplot(
            df[pair_columns], x_vars=["age", "bmi", "children"],
            y_vars=["charges"], hue="smoker", height=3.2,
            plot_kws={"alpha": 0.5, "s": 17},
        )
        g.figure.suptitle("Features vs. Target Charges (by Smoker)", y=1.06)
        g.figure.savefig(folder / "02_pairplot_features_target.png", dpi=160, bbox_inches="tight")
        plt.close(g.figure)

    df_encoded = df.copy()
    encoders = {}
    print("\nLABEL ENCODING:")
    for col in CATEGORICAL:
        encoder = LabelEncoder()
        df_encoded[col] = encoder.fit_transform(df_encoded[col])
        encoders[col] = encoder
        print(f"  {col}: {dict(enumerate(encoder.classes_))}")
    print("\nENCODED DATAFRAME:\n", df_encoded.head())
    if draw_plots:
        fig, ax = plt.subplots(figsize=(9, 6))
        sns.heatmap(df_encoded.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
        ax.set_title("Correlation Heatmap (Label Encoded Data)")
        fig.tight_layout()
        fig.savefig(folder / "03_correlation_heatmap.png", dpi=180)
        plt.close(fig)

    print("\nSTEP 2 - TRAIN / TEST SPLIT")
    X = df_encoded.drop(columns="charges")
    y = df_encoded["charges"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.70, test_size=0.30, random_state=23
    )
    print("X_train:", X_train.shape, "X_test:", X_test.shape)

    print("\nSTEP 3 - MODEL TRAINING")
    model = LinearRegression()
    model.fit(X_train, y_train)

    print("\nSTEP 4 - MODEL TESTING")
    print("Intercept:", model.intercept_)
    print("Coefficients:\n", pd.Series(model.coef_, index=X.columns, name="Coefficient"))
    predictions = model.predict(X_test)
    real_values = y_test.to_numpy()
    comparison = pd.DataFrame({
        "Real_Values": real_values,
        "Predictions": predictions,
        "Residuals": real_values - predictions,
    })
    print("\nPredictions (all test rows):\n", np.round(predictions, 2))
    print("\nReal_Values (all test rows):\n", np.round(real_values, 2))
    print("\nComparison preview:\n", comparison.head(15).round(2))
    comparison.to_csv(folder / "predictions_vs_real_values.csv", index=False)

    if draw_plots:
        fig, ax = plt.subplots(figsize=(7.5, 6))
        sns.scatterplot(x=real_values, y=predictions, alpha=0.55, s=35, ax=ax)
        low = min(real_values.min(), predictions.min())
        high = max(real_values.max(), predictions.max())
        ax.plot([low, high], [low, high], linestyle="--", color="firebrick", label="Perfect prediction")
        ax.set(xlabel="Real Values (USD)", ylabel="Predictions (USD)", title="Real vs. Predicted Medical Costs")
        ax.legend()
        fig.tight_layout()
        fig.savefig(folder / "04_actual_vs_predicted.png", dpi=180)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(8.5, 5))
        sns.histplot(comparison["Residuals"], bins=30, kde=True, color="#246a91", ax=ax)
        ax.axvline(0, color="firebrick", linestyle="--", linewidth=1.5)
        ax.set(xlabel="Residual (Real - Predicted) (USD)", ylabel="Count", title="Residual Histogram")
        fig.tight_layout()
        fig.savefig(folder / "05_residual_histogram.png", dpi=180)
        plt.close(fig)

    print("\nSTEP 5 - MODEL EVALUATION")
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)
    metrics = pd.DataFrame({"Metric": ["MAE", "MSE", "RMSE", "R2"], "Value": [mae, mse, rmse, r2]})
    print(metrics.to_string(index=False))
    metrics.to_csv(folder / "evaluation_metrics.csv", index=False)
    pd.DataFrame({"Feature": X.columns, "Coefficient": model.coef_}).to_csv(
        folder / "model_coefficients.csv", index=False
    )
    return comparison, metrics, df_encoded, model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="insurance.csv")
    parser.add_argument("--output", default="results")
    parser.add_argument("--no-plots", action="store_true")
    args = parser.parse_args()
    df = read_insurance_data(args.data)
    generate_report(df, args.output, draw_plots=not args.no_plots)


if __name__ == "__main__":
    main()