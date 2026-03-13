import pandas as pd

def parse_vintage_date(col_name: str) -> pd.Timestamp:
    """
    Helper function to convert vintage column names like 'PCPI04M1' 
    into a Pandas Timestamp for comparison.
    """
    # Only process columns that start with 'PCPI'
    if not col_name.startswith('PCPI'):
        return None
    
    try:
        # Extract the year (YY) and month (M) parts
        yy_str = col_name[4:6]
        # Month could be 1 or 2 digits, so we slice to the end
        mm_str = col_name[7:] 
        
        # Handle the century pivot (assuming values > 50 are 19xx, else 20xx)
        yy = int(yy_str)
        year = 1900 + yy if yy > 50 else 2000 + yy
        month = int(mm_str)
        
        # Default to the first of the month for comparison
        return pd.Timestamp(year=year, month=month, day=1)
    except ValueError:
        return None

def get_latest_data(pull_date: str, filepath: str = 'data/cpi_data.csv') -> pd.DataFrame:
    """
    Reads CPI data and returns the latest vintage available up to the pull_date.
    Returns a DataFrame with exactly two columns: 'dates' and 'cpi'.
    """
    target_date = pd.to_datetime(pull_date)
    
    # 1. Load the raw data (Change to read_excel if your source is an .xlsx file)
    df = pd.read_csv(filepath)
    
    # 2. Map valid vintage columns to their parsed release dates
    vintage_dates = {}
    for col in df.columns:
        v_date = parse_vintage_date(col)
        # Keep it if it's a valid date AND released on or before our pull_date
        if v_date is not None and v_date <= target_date:
            vintage_dates[col] = v_date
            
    if not vintage_dates:
        raise ValueError(f"No vintage data available on or before pull_date: {pull_date}")
        
    # 3. Find the column with the maximum (most recent) date
    latest_vintage_col = max(vintage_dates, key=vintage_dates.get)
    
    # 4. Extract just the observation date and the chosen vintage column
    # Ensure your source file's first column is actually named 'DATE'
    result_df = df[['DATE', latest_vintage_col]].copy()
    
    # 5. Rename to match lab requirements exactly
    result_df.columns = ['dates', 'cpi']
    
    # 6. Clean up: Convert #N/A to actual NaNs, drop them, and reset index
    # pd.to_numeric with 'coerce' safely turns strings like '#N/A' into NaN
    result_df['cpi'] = pd.to_numeric(result_df['cpi'], errors='coerce')
    result_df = result_df.dropna(subset=['cpi']).reset_index(drop=True)
    
    # Optional: Format the 'dates' column from '2003:09' to standard Datetime
    # result_df['dates'] = pd.to_datetime(result_df['dates'].str.replace(':', '-') + '-01')
    
    return result_df

if __name__ == "__main__":
    # Quick manual test block. 
    # Run `python get_latest_data.py` to test if it fetches PCPI04M1 correctly.
    try:
        test_df = get_latest_data('2004-01-15')
        print(f"Success! Fetched {len(test_df)} rows.")
        print(test_df.head())
    except FileNotFoundError:
        print("Please ensure your data file is placed at 'data/cpi_data.csv'")
