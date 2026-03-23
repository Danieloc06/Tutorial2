import os
import requests
import psycopg2
from datetime import time
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
DATABASE_URL = os.getenv("DATABASE_URL")
def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# 1. Initialize the Flask app
app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")


@app.route('/')
def home():
    # This is the "Homepage"
    return "<h1>Movie API is running!</h1><p>Add /search?t=Inception to the URL to test.</p>"


@app.route('/search')
def search():
    title = request.args.get('t')

    if not title:
        return {"error": "No title provided"}, 400

    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)

    return response.json()


# This part allows you to run it directly from PyCharm
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/ready")
def ready():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()

        return jsonify({"status": "ready"}), 200

    except Exception as e:
        return jsonify({
            "status": "unready",
            "error": str(e)
        }), 500

@app.route("/status")
def status():
    uptime = round(time.time())
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM movies")
                movie_count = cur.fetchone()[0]

        db_status = f"connected ({movie_count} movies)"

    except Exception:
        db_status = "database unavailable"

    return jsonify({
        "service": "DeployHub Movie Service",
        "uptime_seconds": uptime,
        "database": db_status,
        "movie_api_configured": API_KEY is not None,
        "environment": os.getenv("ENVIRONMENT", "development"),
    })
if __name__ == "__main__":
    app.run(debug=True)