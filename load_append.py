import argparse
import duckdb
from get_latest_data import get_latest_data

def load_append(pull_date: str, db_path: str = 'cpi_database.duckdb'):
    df = get_latest_data(pull_date)
    
    with duckdb.connect(db_path) as con:
        # Create table if it doesn't exist yet
        con.execute("CREATE TABLE IF NOT EXISTS cpi_append (dates VARCHAR, cpi DOUBLE)")
        
        # Find the maximum date currently in the database
        max_date_result = con.execute("SELECT MAX(dates) FROM cpi_append").fetchone()[0]
        
        # Filter the DataFrame to only include rows newer than max_date
        if max_date_result is not None:
            df = df[df['dates'] > max_date_result]
        
        # Append the new rows
        if not df.empty:
            con.execute("INSERT INTO cpi_append SELECT * FROM df")
            print(f"[Append] Appended {len(df)} new rows into cpi_append as of {pull_date}")
        else:
            print(f"[Append] No new rows to append as of {pull_date}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load CPI data using Append method.')
    parser.add_argument('--date', type=str, required=True, help='Pull date in YYYY-MM-DD format')
    args = parser.parse_args()
    
    load_append(args.date)
