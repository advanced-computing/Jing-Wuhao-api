# Jing Bu-Wuhao Xia-API

## NYPD Arrest Data API
This is a Flask-based REST API developed for the Advanced Computing for Policy Lab. It serves the 8h9b-rp9u (1).csv dataset, allowing users to query, filter, and export arrest records.

## 🚀 Getting Started
1. Installation
Ensure you have Python installed, then install the required libraries:
pip install flask pandas

2. Run the API
Make sure the CSV file is in the same directory as app.py, then run:
python app.py

The server will start at http://127.0.0.1:5000.

## 🛠 API Functionality & Endpoints
1. List Records
Endpoint: GET /records

Returns a list of arrest records. By default, it returns the first 10 records in JSON format.

2. Filter Data
You can filter the dataset by any column name present in the CSV (e.g., arrest_boro, perp_sex, age_group).

Example: GET /records?arrest_boro=K (Filters for Brooklyn arrests)

Example: GET /records?perp_sex=F&age_group=25-44

3. Pagination (Limit & Offset)
Control the number of results and skip records for large datasets.

limit: Number of records to return (Default: 10).

offset: Number of records to skip (Default: 0).

Example: GET /records?limit=5&offset=20

4. Output Format
Specify whether you want the data returned as JSON or as a downloadable CSV.

format: json (default) or csv.

Example: GET /records?format=csv

5. Retrieve Single Record
Endpoint: GET /records/<arrest_key>

Retrieves full details for a specific arrest using its unique identifier.

Example: GET /records/298699272

## 📊 Dataset Schema
The API processes the following key fields:
| Field | Description |
| :--- | :--- |
| arrest_key | Unique Identifier (Primary Key) |
| arrest_date | Date of the arrest incident |
| pd_desc | Description of the offense |
| arrest_boro | Borough (B: Bronx, S: Staten Island, K: Brooklyn, M: Manhattan, Q: Queens) |
| perp_race | Perpetrator race description |

## 🧪 Testing Checklist
To verify the implementation, test the following URLs in your browser:

[ ] Home Page: http://127.0.0.1:5000/

[ ] JSON List: http://127.0.0.1:5000/records?limit=5

[ ] CSV Export: http://127.0.0.1:5000/records?format=csv

[ ] Filtering: http://127.0.0.1:5000/records?arrest_boro=M

[ ] Single ID: http://127.0.0.1:5000/records/298704325

## Lab Group Members:
[Jing Bu] [Wuhao Xia]