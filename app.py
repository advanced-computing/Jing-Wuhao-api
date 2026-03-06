import pandas as pd
from flask import Flask, request, Response, jsonify
import duckdb

app = Flask(__name__)
DB_NAME = "api_database.duckdb"


def format_output(dataframe, output_format):
    if output_format.lower() == "csv":
        content = dataframe.to_csv(index=False)
        return Response(content, mimetype="text/csv")
    else:
        content = dataframe.to_json(orient="records")
        return Response(content, mimetype="application/json")


@app.route("/records", methods=["GET"])
def list_records():
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    output_format = request.args.get("format", "json")

    query = "SELECT * FROM main_data"
    conditions = []
    params = []
    reserved_keys = ["limit", "offset", "format"]

    for key, value in request.args.items():
        if key not in reserved_keys:
            conditions.append(f"{key} = ?")
            params.append(value)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += f" LIMIT {limit} OFFSET {offset}"

    with duckdb.connect(DB_NAME) as conn:
        if params:
            data = conn.execute(query, params).df()
        else:
            data = conn.sql(query).df()

    return format_output(data, output_format)


@app.route("/records/<int:identifier>", methods=["GET"])
def get_single_record(identifier):
    with duckdb.connect(DB_NAME) as conn:
        query = f"SELECT * FROM main_data WHERE arrest_key = {identifier}"
        record = conn.sql(query).df()

    if record.empty:
        return jsonify({"error": "Identifier not found"}), 404

    return Response(record.iloc[0].to_json(), mimetype="application/json")


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    age = data.get("age")
    country = data.get("country")

    if not all([username, age, country]):
        return jsonify({"error": "Missing data"}), 400

    with duckdb.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO users (username, age, country) VALUES (?, ?, ?)",
            (username, age, country),
        )

    return jsonify({"message": f"User {username} added successfully!"}), 201


@app.route("/users/stats", methods=["GET"])
def get_user_stats():
    with duckdb.connect(DB_NAME) as conn:
        total_users = conn.sql("SELECT COUNT(*) FROM users").fetchone()[0]

        avg_age = conn.sql("SELECT AVG(age) FROM users").fetchone()[0]
        avg_age = float(avg_age) if avg_age else 0.0

        top_countries_data = conn.sql("""
            SELECT country, COUNT(*) as user_count 
            FROM users 
            GROUP BY country 
            ORDER BY user_count DESC 
            LIMIT 3
        """).fetchall()

    top_countries = [{"country": row[0], "count": row[1]} for row in top_countries_data]

    return jsonify(
        {
            "total_users": total_users,
            "average_age": round(avg_age, 2),
            "top_3_countries": top_countries,
        }
    ), 200


@app.route("/")
def index():
    return jsonify({"message": "API is running. DuckDB is connected!"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
