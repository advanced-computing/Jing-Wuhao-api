import pandas as pd
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

# Load the dataset once at startup
CSV_FILE = "8h9b-rp9u (1).csv"
df = pd.read_csv(CSV_FILE)


# 1. Filter the data based on a particular column
def apply_filters(dataframe, query_params):
    """Filters dataframe based on query parameters matching column names."""
    filtered_df = dataframe.copy()
    reserved_keys = ["limit", "offset", "format"]

    for key, value in query_params.items():
        if key in filtered_df.columns and key not in reserved_keys:
            if filtered_df[key].dtype == "int64":
                filtered_df = filtered_df[filtered_df[key] == int(value)]
            else:
                filtered_df = filtered_df[filtered_df[key].astype(str) == str(value)]
    return filtered_df


# 2. Specify a limit and offset
def apply_pagination(dataframe, limit, offset):
    return dataframe.iloc[offset : offset + limit]


# 3. Specify the output format (CSV or JSON)
def format_output(dataframe, output_format):
    if output_format.lower() == "csv":
        content = dataframe.to_csv(index=False)
        return Response(content, mimetype="text/csv")
    else:
        # Default to JSON
        content = dataframe.to_json(orient="records")
        return Response(content, mimetype="application/json")


# 4. List records (The main endpoint)
@app.route("/records", methods=["GET"])
def list_records():
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    output_format = request.args.get("format", "json")

    # Chain the logic functions
    data = apply_filters(df, request.args)
    data = apply_pagination(data, limit, offset)

    return format_output(data, output_format)


# 5. Retrieve a single record by identifier
@app.route("/records/<int:identifier>", methods=["GET"])
def get_single_record(identifier):
    record = df[df["arrest_key"] == identifier]

    if record.empty:
        return jsonify({"error": "Identifier not found"}), 404

    return Response(record.iloc[0].to_json(), mimetype="application/json")


# Home route to prevent 404 on the root URL
@app.route("/")
def index():
    return jsonify({"message": "API is running. Use /records to view data."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
