# CPI Data Pipeline: DuckDB Loading Strategies

## Overview
This project continuously loads and updates Consumer Price Index (CPI) data from the Philadelphia Federal Reserve into a DuckDB database. It implements and compares three data loading strategies: Truncate, Append, and Incremental.

## Usage Instructions
Ensure your Python environment has the necessary dependencies installed (e.g., `pandas`, `duckdb`). 
All scripts accept a `--date` parameter (format: `YYYY-MM-DD`) representing the simulated `pull_date`.

Run the scripts from the root directory:
```bash
python scripts/load_trunc.py --date 2004-01-15
python scripts/load_append.py --date 2004-01-15
python scripts/load_inc.py --date 2004-01-15
