"""EDA Mini Project | Seaborn Tips dataset | 6 charts + 12 data-grounded insights.
Dependencies: pandas, numpy, matplotlib, seaborn
Run: python EDA_Tips_Project.py
Keep tips.csv next to this file (or permit seaborn to download the example dataset).
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.05)
plt.rcParams.update({"figure.dpi": 115, "savefig.dpi": 180, "axes.titleweight": "bold", "axes.spines.top": False, "axes.spines.right": False})

file_path = Path(__file__).resolve().parent / "tips.csv"
if file_path.exists():
    df = pd.read_csv(file_path)
else:
    # In Google Colab, seaborn downloads its bundled example dataset if no local CSV was uploaded.
    df = sns.load_dataset("tips")

df["day"] = pd.Categorical(df["day"], categories=["Thur", "Fri", "Sat", "Sun"], ordered=True)
assert set(["total_bill", "tip", "sex", "smoker", "day", "time", "size"]).issubset(df.columns)
print("Data shape:", df.shape)
print("Missing values by column:\n", df.isna().sum())
print("Numerical summary:\n", df.select_dtypes(include="number").describe().round(2))

OUTPUT_DIR = Path(__file__).resolve().parent / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)


# 1) Univariate: distribution of total bill
fig, ax = plt.subplots(figsize=(9, 5.2))
sns.histplot(data=df, x="total_bill", bins=18, color="#317E96", edgecolor="white", alpha=.88, ax=ax)
ax.axvline(df["total_bill"].mean(), color="#B5433A", lw=2.4, ls="--", label=f"Mean = {df['total_bill'].mean():.2f}")
ax.axvline(df["total_bill"].median(), color="#D99C3D", lw=2.4, ls=":", label=f"Median = {df['total_bill'].median():.2f}")
ax.set(title="Univariate analysis | Bill distribution", xlabel="Total bill", ylabel="Number of bills")
ax.legend(frameon=True)
fig.tight_layout()

fig.savefig(OUTPUT_DIR / "01_univariate_bill_histogram.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# 2) Univariate: frequency of observations by day
fig, ax = plt.subplots(figsize=(9, 5.2))
counts = df["day"].value_counts().reindex(["Thur", "Fri", "Sat", "Sun"])
bars = ax.bar(counts.index.astype(str), counts.values, color=["#6AA5AE", "#A7C5C5", "#2F758A", "#D59B54"], width=.7)
for bar, n in zip(bars, counts.values):
    ax.text(bar.get_x()+bar.get_width()/2, n+1, f"{n} ({n/len(df):.1%})", ha="center", fontsize=10, fontweight="bold")
ax.set_ylim(0, max(counts.values)*1.19)
ax.set(title="Univariate analysis | Bills by day", xlabel="Day", ylabel="Number of bills")
fig.tight_layout()

fig.savefig(OUTPUT_DIR / "02_univariate_day_counts.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# 3) Bivariate: total bill vs. tip
fig, ax = plt.subplots(figsize=(9, 5.2))
sns.regplot(data=df, x="total_bill", y="tip", ax=ax,
            scatter_kws={"alpha": .55, "s": 45, "color": "#317E96"},
            line_kws={"color": "#B5433A", "lw": 2.4}, ci=None)
r = df["total_bill"].corr(df["tip"])
ax.text(.03,.94,f"Pearson r = {r:.3f}", transform=ax.transAxes,
        bbox={"boxstyle":"round,pad=.4", "facecolor":"white", "edgecolor":"#CDDBDE"})
ax.set(title="Bivariate analysis | Total bill vs. tip", xlabel="Total bill", ylabel="Tip")
fig.tight_layout()

fig.savefig(OUTPUT_DIR / "03_bivariate_bill_tip_scatter.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# 4) Bivariate: tip distribution by day
fig, ax = plt.subplots(figsize=(9, 5.2))
sns.boxplot(data=df, x="day", y="tip", order=["Thur", "Fri", "Sat", "Sun"],
            color="#80B7C1", width=.53, showfliers=True, ax=ax)
ax.set(title="Bivariate analysis | Tip distribution by day", xlabel="Day", ylabel="Tip")
fig.tight_layout()

fig.savefig(OUTPUT_DIR / "04_bivariate_tip_boxplot_day.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# 5) Multivariate: 4 variables (bill, tip, meal time, party size)
fig, ax = plt.subplots(figsize=(9, 5.2))
sns.scatterplot(data=df, x="total_bill", y="tip", hue="time", size="size", sizes=(35, 220),
                palette={"Lunch":"#3B96A7", "Dinner":"#D28B51"}, alpha=.73, edgecolor="white", linewidth=.45, ax=ax)
ax.set(title="Multivariate analysis | Bill, tip, time and party size", xlabel="Total bill", ylabel="Tip")
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), borderaxespad=0, title="Time / size")
fig.tight_layout()

fig.savefig(OUTPUT_DIR / "05_multivariate_scatter_time_party.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# 6) Multivariate: average tip by day and sex
fig, ax = plt.subplots(figsize=(9, 5.2))
sns.barplot(data=df, x="day", y="tip", hue="sex", order=["Thur", "Fri", "Sat", "Sun"],
            hue_order=["Female", "Male"], errorbar=None, palette={"Female":"#D19464", "Male":"#377E93"}, ax=ax)
means = df.groupby(["day", "sex"], observed=True)["tip"].mean()
for bar in ax.patches:
    height = bar.get_height()
    if np.isfinite(height) and height > 0.01:
        ax.text(bar.get_x()+bar.get_width()/2, height+.045, f"{height:.2f}", ha="center", fontsize=9)
ax.set_ylim(0, 4.1)
ax.set(title="Multivariate analysis | Mean tip by day and sex", xlabel="Day", ylabel="Average tip")
ax.legend(title="Sex")
fig.tight_layout()

fig.savefig(OUTPUT_DIR / "06_multivariate_mean_tip_day_sex.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# Concise diagnostics / descriptive findings
print("\n--- Summary for interpretation ---")
print("Total bills < 25:", (df.total_bill < 25).sum())
print("Day counts:\n", df.day.value_counts())
print("Bill-tip correlation:", round(df.total_bill.corr(df.tip), 3))
print("Median tips by day:\n", df.groupby("day", observed=True).tip.median())
print("Average bill by time:\n", df.groupby("time").total_bill.mean())
print("Average bill by party size:\n", df.groupby("size").total_bill.mean())
print("Average tips by day and sex:\n", df.groupby(["day", "sex"], observed=True).tip.mean())
print(f"Saved {len(list(OUTPUT_DIR.glob('*.png')))} charts in {OUTPUT_DIR}")