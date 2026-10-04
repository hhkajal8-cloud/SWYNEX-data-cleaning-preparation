# SWYNEX Technologies — Data Analyst Internship
## Task 1: Data Cleaning & Preparation

**Intern:** Kajal
**Objective:** Clean and prepare a raw retail sales dataset for analysis.

## Dataset
- Source: [Kaggle](https://www.kaggle.com/) — *Retail Store Sales (Dirty)* dataset (or the public dataset you chose — update this line)
- Columns: Transaction ID, Customer ID, Category, Item, Price Per Unit, Quantity, Total Spent, Payment Method, Location, Transaction Date, Discount Applied

## Data Quality Issues Identified
1. **Duplicate records** — exact repeated rows (same Transaction ID)
2. **Missing values** — in Customer ID, Price Per Unit, Quantity, Discount Applied
3. **Incorrect data types** — dates and numeric columns stored as text
4. **Inconsistent values** — inconsistent capitalization/spacing in category and location fields, mixed date formats, and a Total Spent column that didn't always equal Price × Quantity

## Cleaning Steps (Python / Pandas)
1. Parsed `Transaction Date` into proper datetime format and coerced Price/Quantity/Total Spent to numeric
2. Standardized text fields (trimmed whitespace, consistent title case) across Category, Item, Payment Method, and Location
3. Normalized `Discount Applied` to boolean True/False
4. Filled missing `Quantity` with the column median, and missing `Price Per Unit` with the median price for that item
5. Recomputed `Total Spent` wherever it was missing or didn't match Price × Quantity
6. Dropped rows missing an irrecoverable identifier (Transaction ID, Customer ID, or Transaction Date)
7. Removed duplicate transactions
8. Exported the result to `cleaned_data.csv`

## Tools Used
Python, Pandas

## How to Run
```bash
pip install pandas
python clean_data.py
```
Place your raw file as `raw_data.csv` in the same folder before running.

## Files
- `raw_data.csv` — original dataset
- `clean_data.py` — cleaning script
- `cleaned_data.csv` — cleaned output
