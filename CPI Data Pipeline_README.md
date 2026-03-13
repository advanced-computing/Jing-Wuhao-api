# CPI Data Loading to DuckDB

## Overview
This project continuously loads and updates Consumer Price Index (CPI) data from the Philadelphia Federal Reserve into a DuckDB database. We are implementing and comparing three different data loading strategies: Truncate, Append, and Incremental.

## Usage Instructions
All data loading scripts are designed to accept a `pull_date` parameter (format: YYYY-MM-DD). 

To run the scripts manually from the command line:
`python load_trunc.py --pull_date 2004-01-15`
`python load_append.py --pull_date 2004-01-15`
`python load_inc.py --pull_date 2004-01-15`

## Manual Testing & Expected Outcomes

All scripts interact with the source data exclusively through a central function: `get_latest_data(pull_date)`. This function returns a two-column table (`dates`, `cpi`) representing the latest vintage of data available up to that specific pull date.

Here is what to expect in the DuckDB tables after running each script:

### 1. Truncate (`load_trunc.py`)
* **Behavior:** Drops the existing table completely and recreates it using the data returned by `get_latest_data`.
* **Expected Table State:** The table will perfectly match the latest available data, including all historical revisions. 
* **Idempotency:** Running it multiple times for the same date will not duplicate data.

### 2. Append (`load_append.py`)
* **Behavior:** Checks the maximum date currently in the database table and only inserts new rows that have a date strictly greater than that maximum date.
* **Expected Table State:** The table will contain new monthly observations, but **it will not reflect historical revisions** (which usually happen in February). 
* **Idempotency:** Running it multiple times for the same date will not duplicate data because it only appends dates newer than what is already stored.

### 3. Incremental (`load_inc.py`)
* **Behavior:** Uses an "upsert" (update or insert) logic. It adds new monthly observations and updates any existing historical rows if their CPI values have been revised in the source data.
* **Expected Table State:** Like Truncate, the table will perfectly match the latest available data and capture all historical revisions. However, it achieves this without dropping the entire table.
* **Idempotency:** Running it multiple times will safely overwrite existing data with the exact same data, resulting in no duplicates.
