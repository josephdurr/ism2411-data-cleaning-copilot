import os
import sys

# Ensure `src` is importable for tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_cleaning import load_data, clean_column_names, handle_missing_values, remove_invalid_rows


def test_cleaning_pipeline_produces_valid_rows():
    raw_path = os.path.join('data', 'raw', 'sales_data_raw.csv')
    df = load_data(raw_path)
    df = clean_column_names(df)
    df = handle_missing_values(df)
    df = remove_invalid_rows(df)

    # Find columns
    price_col = next((c for c in df.columns if 'price' in c), None)
    qty_col = next((c for c in df.columns if 'quantity' in c or 'qty' in c), None)

    assert price_col is not None, "Price column not found after cleaning"
    assert qty_col is not None, "Quantity column not found after cleaning"

    # No non-positive prices or quantities should remain
    assert (df[price_col] > 0).all(), "Non-positive price found in cleaned data"
    assert (df[qty_col] > 0).all(), "Non-positive quantity found in cleaned data"
