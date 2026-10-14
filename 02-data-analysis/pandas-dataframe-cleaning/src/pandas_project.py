import pandas as pd
import numpy as np

# 1. Create a DataFrame with 15 rows and 3 columns.
# The first 9 records are from the assignment; the last 6 are sample records.
data = {
    "Level": pd.Series([
        100, 100, 100, 200, pd.NA, 200, 300, 300, pd.NA,
        300, 200, 300, 400, 400, 200
    ], dtype="Int64"),
    "Course Name": [
        "Introduction to IT",
        "Programming Fundamentals",
        "Introduction to MIS",
        "Database Management",
        "Data Structures",
        "Systems Analysis and Design",
        "Network Security",
        "Algorithms",
        np.nan,
        "Cloud Computing",
        "Web Development",
        "Business Intelligence",
        "Machine Learning",
        "IT Project Management",
        "Cybersecurity Fundamentals",
    ],
    "Major": [
        "IT", "CS", "MIS", np.nan, "CS", "MIS", np.nan, "CS", np.nan,
        "IT", "CS", "MIS", "CS", "IT", "IT"
    ],
}

df = pd.DataFrame(data)

print("1. Original DataFrame (15 rows x 3 columns):")
print(df.to_string(index=False))
print("\nShape:", df.shape)

# 2. Print descriptive statistics for all columns.
print("\n2. DataFrame describe (all columns):")
print(df.describe(include="all").to_string())

# 3. Convert the Level column to double precision (float64).
df["Level"] = df["Level"].astype("float64")
print("\n3. Level data type after conversion:", df["Level"].dtype)

# 4. Display the first four rows.
print("\n4. First four rows:")
print(df.head(4).to_string(index=False))

# 5. Remove every row with one or more missing values.
clean_df = df.dropna()
print("\n5. DataFrame after dropna():")
print(clean_df.to_string(index=False))
print("\nRemaining rows:", len(clean_df))
print("Missing values after cleaning:", int(clean_df.isna().sum().sum()))