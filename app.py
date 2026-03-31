import os
import requests
import psycopg2
import time
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import psycopg2.extras


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
def get_conn():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

# 1. Initialize the Flask app
app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/index/')
def index():
    return render_template("index.html")



@app.route('/search')
def search():
    title = request.args.get('t')
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}")
    data = response.json()

    if not title:
        return {"error": "No title provided"}, 400
    if data.get("Response") == "True":
        insert_movie(data)
    return render_template("index.html", content=data)


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

def insert_movie(data):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO unnormalised_movie 
        (movie_title, movie_year, movie_rated, movie_released, movie_runtime, movie_genres, movie_directors, movie_writers, movie_actors, movie_plot, movie_poster, movie_imdb_rating, movie_imdb_id, movie_box_office)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("Title"),
        data.get("Year"),
        data.get("Rated"),
        data.get("Released"),
        data.get("Runtime"),
        data.get("Genre"),
        data.get("Director"),
        data.get("Writer"),
        data.get("Actors"),
        data.get("Plot"),
        data.get("Poster"),
        data.get("imdbRating"),
        data.get("imdbID"),
        data.get("BoxOffice")
    ))
    conn.commit()
    conn.close()

@app.route('/view/')
def view():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM unnormalised_movie')
    unnormalised_movie = cur.fetchall()
    conn.close()
    return render_template('view.html', unnormalised_movie=unnormalised_movie)

if __name__ == "__main__":
    app.run(debug=True)