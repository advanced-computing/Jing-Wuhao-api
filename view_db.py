import duckdb

conn = duckdb.connect("api_database.duckdb")

print("--- USERS TABLE ---")
conn.sql("SELECT * FROM users").show()

print("\n--- MAIN DATA TABLE (first 5 rows) ---")
conn.sql("SELECT * FROM main_data LIMIT 5").show()

conn.close()
