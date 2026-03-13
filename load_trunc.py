import argparse
import duckdb
from get_latest_data import get_latest_data

def load_trunc(pull_date: str, db_path: str = 'cpi_database.duckdb'):
    # 1. Fetch the latest data using the centralized function
    df = get_latest_data(pull_date)
    
    # 2. Connect to DuckDB
    with duckdb.connect(db_path) as con:
        # DuckDB can directly query Pandas DataFrames. 
        # CREATE OR REPLACE will drop the existing table and recreate it.
        con.execute("CREATE OR REPLACE TABLE cpi_trunc AS SELECT * FROM df")
        
        # Verify the load
        count = con.execute("SELECT COUNT(*) FROM cpi_trunc").fetchone()[0]
        print(f"[Truncate] Loaded {count} rows into cpi_trunc as of {pull_date}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load CPI data using Truncate method.')
    parser.add_argument('--date', type=str, required=True, help='Pull date in YYYY-MM-DD format')
    args = parser.parse_args()
    
    load_trunc(args.date)
