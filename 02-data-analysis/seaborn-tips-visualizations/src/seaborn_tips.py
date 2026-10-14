"""Seaborn Tips Dataset — Histogram, Displot, ECDF.

Run: python Seaborn_Tips_Project.py
Requires: pandas, matplotlib, seaborn
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1) Read the tips dataset from Seaborn.
# If offline, read the same dataset from the provided tips.csv file.
try:
    tips = sns.load_dataset("tips")
except Exception:
    tips = pd.read_csv(BASE_DIR / "tips.csv")

print("Dataset shape:", tips.shape)
print(tips.head().to_string(index=False))

# 2) Histogram: tip on x-axis; categories separated by day.
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=tips, x="tip", hue="day", element="step", ax=ax)
ax.set_title("Tip Distribution by Day")
ax.set_xlabel("Tip")
ax.set_ylabel("Count")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "01_histogram_tip_by_day.png", dpi=200)
plt.show()
plt.close(fig)

# 3) Displot: day on x-axis; grouped by sex, with the requested styling.
sns.set_theme(style="whitegrid")
g = sns.displot(
    data=tips,
    x="day",
    hue="sex",
    hue_order=["Female", "Male"],
    multiple="dodge",
    shrink=0.8,
    palette="Set1",
    height=5,
    aspect=1.6,
)
g.set_axis_labels("Day", "Count")
g.figure.suptitle("Number of Records by Day and Sex", y=1.03)
g.figure.savefig(OUTPUT_DIR / "02_displot_day_by_sex.png", dpi=200, bbox_inches="tight")
plt.show()
plt.close(g.figure)

# 4) ECDF: tip on x-axis; line colors from the 'summer' colormap.
sns.set_theme(style="darkgrid", font_scale=1.25)
fig, ax = plt.subplots(figsize=(10, 6))
sns.ecdfplot(
    data=tips,
    x="tip",
    hue="time",
    palette="summer",
    linewidth=3,
    ax=ax,
)
ax.set_title("ECDF of Tips by Meal Time")
ax.set_xlabel("Tip")
ax.set_ylabel("Proportion")
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "03_ecdf_tip_by_time.png", dpi=200)
plt.show()
plt.close(fig)

print("Saved all three charts to:", OUTPUT_DIR)