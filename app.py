from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

app = Flask(__name__)

# Database connection URL
db_url = 'postgres://crime_data_user:42RVMbzKCACMk5mwWpv4xI24pCN3WXnk@dpg-cntrluvsc6pc7392206g-a.oregon-postgres.render.com/crime_data'

# Function to create the camera_data table
def create_table():
    conn = psycopg2.connect(db_url)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS camera_data (
            id SERIAL PRIMARY KEY,
            location VARCHAR(100) NOT NULL,
            cameraid VARCHAR(50) NOT NULL,
            timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.close()
    conn.close()

# Ensure the table is created before the first request


# Endpoint to insert data
@app.route('/insert', methods=['POST'])
def insert_data():
    if request.is_json:
        data = request.get_json()
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()
            query = """
                INSERT INTO camera_data (location, cameraid, timestamp)
                VALUES (%s, %s, %s);
            """
            cursor.execute(query, (data['location'], data['cameraid'], datetime.utcnow()))
            conn.commit()
            cursor.close()
            return jsonify({"message": "Data inserted successfully!"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if conn is not None:
                conn.close()
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)