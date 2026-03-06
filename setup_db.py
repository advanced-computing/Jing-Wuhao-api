import duckdb

db_name = "api_database.duckdb"
conn = duckdb.connect(db_name)

csv_filename = "8h9b-rp9u (1).csv"
conn.sql(f"CREATE TABLE main_data AS SELECT * FROM read_csv_auto('{csv_filename}')")

conn.sql("""
    CREATE TABLE users (
        username VARCHAR,
        age INTEGER,
        country VARCHAR
    )
""")

conn.close()
