"""
SWYNEX Technologies - Data Analyst Internship
Task 1: Data Cleaning & Preparation

Dataset: Retail Store Sales (raw/dirty transaction data)
Author: Kajal
"""

import numpy as np
import pandas as pd

RAW_FILE = "raw_data.csv"
CLEAN_FILE = "cleaned_data.csv"

# ---------------------------------------------------------------
# 1. Load raw data and get a first look at the problems
# ---------------------------------------------------------------
df = pd.read_csv(RAW_FILE)
print("Raw shape:", df.shape)
print("\nMissing values per column:\n", df.isnull().sum())
print("\nDtypes:\n", df.dtypes)
print("\nDuplicate rows:", df.duplicated().sum())

df.columns = df.columns.str.strip()

# ---------------------------------------------------------------
# 2. Fix data types (dates and numbers often load as text)
# ---------------------------------------------------------------
df["Transaction Date"] = pd.to_datetime(
    df["Transaction Date"], errors="coerce", format="mixed"
)

for col in ["Price Per Unit", "Quantity", "Total Spent"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------------------------------------------
# 3. Standardize text/categorical values
#    (extra spaces, inconsistent casing, stray "nan" strings)
# ---------------------------------------------------------------
text_cols = ["Category", "Item", "Payment Method", "Location"]

df["Item"] = df["Item"].fillna("Unknown")
df["Category"] = df["Category"].fillna("Unknown")
df["Payment Method"] = df["Payment Method"].fillna("Unknown")
df["Location"] = df["Location"].fillna("Unknown")

for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.title()
    df[col] = df[col].replace({"Nan": np.nan, "None": np.nan, "": np.nan})

df["Discount Applied"] = (
    df["Discount Applied"].astype(str).str.strip().str.lower().map(
        {"true": True, "1": True, "yes": True,
         "false": False, "0": False, "no": False}
    )
)
df["Discount Applied"] = df["Discount Applied"].fillna(False)

# ---------------------------------------------------------------
# 4. Handle missing values
# ---------------------------------------------------------------
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())

df["Price Per Unit"] = df["Price Per Unit"].fillna(
    df.groupby("Item")["Price Per Unit"].transform("median")
)
df["Price Per Unit"] = df["Price Per Unit"].fillna(df["Price Per Unit"].median())

df["Total Spent"] = df["Total Spent"].fillna(df["Price Per Unit"] * df["Quantity"])

df = df.dropna(subset=["Transaction ID", "Customer ID", "Transaction Date"])

# ---------------------------------------------------------------
# 5. Fix inconsistent values
# ---------------------------------------------------------------
expected_total = df["Price Per Unit"] * df["Quantity"]
mismatch = (df["Total Spent"] - expected_total).abs() > 0.01
df.loc[mismatch, "Total Spent"] = expected_total[mismatch]

# ---------------------------------------------------------------
# 6. Remove duplicate records
# ---------------------------------------------------------------
before = len(df)
df = df.drop_duplicates(subset=["Transaction ID"])
print(f"\nRemoved {before - len(df)} duplicate row(s)")

# ---------------------------------------------------------------
# 7. Final check + export
# ---------------------------------------------------------------
print("\nCleaned shape:", df.shape)
print("Remaining missing values:\n", df.isnull().sum())

df.to_csv(CLEAN_FILE, index=False)
print(f"\nSaved cleaned dataset to {CLEAN_FILE}")