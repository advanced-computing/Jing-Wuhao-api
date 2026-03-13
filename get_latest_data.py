import pandas as pd
import numpy as np


def parse_vintage_date(col_name: str) -> pd.Timestamp:
    """
    Helper function to convert vintage column names like 'PCPI98M11' or 'PCPI04M1'
    into a Pandas Timestamp for comparison.
    """
    if not col_name.startswith("PCPI"):
        return None

    try:
        # P-C-P-I-[YY]-M-[MM]
        # 0 1 2 3  4 5 6  7..
        yy_str = col_name[4:6]
        mm_str = col_name[7:]

        # Handle century pivot: 98 -> 1998, 04 -> 2004
        yy = int(yy_str)
        year = 1900 + yy if yy > 50 else 2000 + yy
        month = int(mm_str)

        return pd.Timestamp(year=year, month=month, day=1)
    except ValueError:
        return None


def get_latest_data(
    pull_date: str, filepath: str = "data/pcpiMvMd.xlsx"
) -> pd.DataFrame:
    """
    Reads CPI Excel data and returns the latest vintage available up to the pull_date.
    """
    target_date = pd.to_datetime(pull_date)

    # 1. Load the Excel data. (Tell pandas to treat '#N/A' as actual NaNs)
    df = pd.read_excel(filepath, na_values=["#N/A"])

    # 2. Map valid vintage columns to their parsed release dates
    vintage_dates = {}
    for col in df.columns:
        v_date = parse_vintage_date(col)
        # Keep it if it's a valid date AND released on or before our pull_date
        if v_date is not None and v_date <= target_date:
            vintage_dates[col] = v_date

    if not vintage_dates:
        raise ValueError(
            f"No vintage data available on or before pull_date: {pull_date}"
        )

    # 3. Find the column with the maximum (most recent) date
    latest_vintage_col = max(vintage_dates, key=vintage_dates.get)
    print(
        f"[*] For pull_date {pull_date}, selected vintage column: {latest_vintage_col}"
    )

    # 4. Extract just the DATE and the chosen vintage column
    result_df = df[["DATE", latest_vintage_col]].copy()

    # 5. Rename to match lab requirements exactly ('dates', 'cpi')
    result_df.columns = ["dates", "cpi"]

    # 6. Standardize the 'dates' column from '1947:01' to standard '1947-01-01'
    # This is crucial for DuckDB sorting and incremental updates
    result_df["dates"] = result_df["dates"].astype(str).str.replace(":", "-") + "-01"

    # 7. Clean up: Convert to numeric, drop missing values, and reset index
    result_df["cpi"] = pd.to_numeric(result_df["cpi"], errors="coerce")
    result_df = result_df.dropna(subset=["cpi"]).reset_index(drop=True)

    return result_df


if __name__ == "__main__":
    # Quick manual test block
    try:
        test_df = get_latest_data("2004-01-15")
        print(f"\nSuccess! Fetched {len(test_df)} rows.")
        print(test_df.head())
        print(test_df.tail())
    except FileNotFoundError:
        print("Error: Please ensure your data file is placed at 'data/pcpiMvMd.xlsx'")
