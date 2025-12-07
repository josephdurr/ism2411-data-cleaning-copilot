"""
data_cleaning.py

Purpose: Load a messy sales CSV, apply a series of cleaning steps,
and write a cleaned CSV to `data/processed/sales_data_clean.csv`.

Cleaning steps include:
- Standardize column names (lowercase, underscores)
- Strip whitespace from text fields
- Handle missing prices and quantities (consistent filling)
- Remove clearly invalid rows (negative prices/quantities)

Comments before each major step explain what and why.
"""
import re
from typing import Optional

import pandas as pd


# Copilot-assisted: load_data
# This function should read a CSV from `file_path` and return a DataFrame.
# It also attempts to coerce common formatting issues (like dollar signs).
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    # Normalize column names temporarily (strip leading/trailing whitespace)
    df.columns = [c.strip() for c in df.columns]

    # Remove surrounding quotes and whitespace from string cells
    str_cols = df.select_dtypes(include=['object']).columns
    for c in str_cols:
        df[c] = df[c].astype(str).str.strip().str.strip('"')

    # Try to coerce common numeric columns that may include dollar signs or text
    if 'PRICE' in df.columns:
        # remove dollar signs and other non-numeric characters for price
        df['PRICE'] = df['PRICE'].replace('', pd.NA)
        df['PRICE'] = df['PRICE'].astype(str).str.replace(r'[^0-9.\-]', '', regex=True)
        df['PRICE'] = pd.to_numeric(df['PRICE'], errors='coerce')

    # Coerce Quantity to numeric
    if 'Quantity' in df.columns:
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names and basic string cleanup.

    What: Lowercase column names and replace spaces with underscores.
    Why: Consistent column names make downstream processing reliable.
    """
    df = df.copy()
    df.columns = [re.sub(r"\s+", "_", c.strip().lower()) for c in df.columns]

    # Strip whitespace from likely textual columns
    for col in ['product_name', 'category']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df


# Copilot-assisted: handle_missing_values
# This function should fill or remove missing values consistently.
# I used Copilot to scaffold the function and then adjusted filling strategies.
def handle_missing_values(df: pd.DataFrame, price_fill: Optional[float] = None) -> pd.DataFrame:
    """Handle missing prices and quantities.

    What: Fill missing `price` with median (or provided `price_fill`).
    Why: Missing prices hinder revenue calculations; median is robust to outliers.

    What: Fill missing `quantity` with 1 (assume a single item) when reasonable.
    Why: Dropping many rows can remove useful data; filling with 1 is a simple, consistent choice.
    """
    df = df.copy()

    # Price column may be named 'price' after cleaning or remain as 'price'
    price_col = None
    for c in df.columns:
        if c == 'price' or c == 'price' or 'price' in c:
            price_col = c
            break

    if price_col:
        if price_fill is None:
            median_price = df[price_col].median(skipna=True)
        else:
            median_price = price_fill
        df[price_col] = df[price_col].fillna(median_price)

    # Quantity column
    qty_col = None
    for c in df.columns:
        if c in ('quantity', 'qty'):
            qty_col = c
            break
    if qty_col:
        df[qty_col] = df[qty_col].fillna(1)

    return df


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with clearly invalid values.

    What: Drop rows with negative or zero quantity or price <= 0.
    Why: These are typically data entry errors or nonsensical for sales data.
    """
    df = df.copy()

    # Identify price and quantity columns robustly
    price_col = next((c for c in df.columns if 'price' in c), None)
    qty_col = next((c for c in df.columns if 'quantity' in c or 'qty' in c), None)

    if qty_col:
        df = df[df[qty_col].notna()]
        df = df[df[qty_col] > 0]

    if price_col:
        df = df[df[price_col].notna()]
        df = df[df[price_col] > 0]

    # Drop rows where product name is empty
    if 'product_name' in df.columns:
        df = df[df['product_name'].notna() & (df['product_name'].str.strip() != '')]

    return df.reset_index(drop=True)


if __name__ == "__main__":
    import os

    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())
