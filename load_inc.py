import argparse
import duckdb
from get_latest_data import get_latest_data

def load_incremental(pull_date: str, db_path: str = 'cpi_database.duckdb'):
    df = get_latest_data(pull_date)
    
    with duckdb.connect(db_path) as con:
        # Create table with PRIMARY KEY for upsert logic
        con.execute("""
            CREATE TABLE IF NOT EXISTS cpi_inc (
                dates VARCHAR PRIMARY KEY, 
                cpi DOUBLE
            )
        """)
        
        # Use DuckDB's native Upsert (INSERT ... ON CONFLICT)
        # If the date doesn't exist, it inserts. 
        # If it exists, it updates the CPI value to handle historical revisions.
        con.execute("""
            INSERT INTO cpi_inc SELECT * FROM df 
            ON CONFLICT (dates) DO UPDATE SET cpi = EXCLUDED.cpi
        """)
        
        print(f"[Incremental] Upserted data into cpi_inc as of {pull_date}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load CPI data using Incremental method.')
    parser.add_argument('--date', type=str, required=True, help='Pull date in YYYY-MM-DD format')
    args = parser.parse_args()
    
    load_incremental(args.date)
