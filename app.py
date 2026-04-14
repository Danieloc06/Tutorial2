import os
import requests
import time
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from dotenv import load_dotenv
from cache_db import cache, init_cache, save_movies_to_local, load_movies_from_local
import psycopg
from psycopg.rows import dict_row

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") #creates variable to connect to supabase database
def get_conn():
    try:
        conn = psycopg.connect(DATABASE_URL, sslmode='require')#uses psycopg3 to establish a connection to database
        return conn
    except (psycopg.OperationalError, psycopg.ProgrammingError):
        return None #try and except clause in the case these errors are raised


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")
init_cache(app)# calls the "init_cache" function

@app.route('/')
def home():
    return render_template("home.html") #renders the homepage

@app.route('/index/')
def index():
    return render_template("index.html") #renders the index page



@app.route('/search')
def search():# function for searching movies using the api
    title = request.args.get('t')# captures the title as the input the user entered
    if not title:
        return {"error": "No title provided"}, 400 # calls an error if no title is provided
    if movie_exists(title):
        flash("Movie in Database!", "success")
        return render_template("index.html") # movie already exists in db and flashes a message to let the user know, the info is not saved again
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}")#uses the input along with the api key to find the movie data
    data = response.json()# movie data is converted to json
    if data.get("Response") == "True":
        saved = insert_movie(data)# if data is found and the database is active then the "insert_movie" function is called
        if saved is False:# if the movie is found but the database is down then the data will display but not be saved
            flash("Movie found but could not be saved! database is unavailable.", "partial_success")
        else:
            flash("Movie added successfully!", "success")# movie is found and server is active, shows a success message to user
    else:
        flash("Movie not found!", "error")# if movie title could not be found using api, could be incorrect spelling etc
    return render_template("index.html", content=data)

def health():
    return jsonify({"status": "ok"})# shows status, not included as a page as I felt it overlapped info with other diagnostics pages

@app.route('/ready')
def ready():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()# tries to connect to database
        return render_template('ready.html',status="ready"), 200# if db is ready then this is returned
    except Exception as e:
        return render_template('ready.html',status="unready", error=str(e)), 500# if db is not ready then this is returned

@app.route("/status")
def status():
    uptime = round(time.time())
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM unnormalised_movie")#checks number of entries (movies in database)
                movie_count = cur.fetchone()[0]

        db_status = f"connected ({movie_count} movies)"

    except Exception:
        db_status = "database unavailable" # try and except clause in case database is down

    return render_template("status.html",
                           service="DeployHub Movie Service",
                           uptime_seconds=uptime,
                           database=db_status,
                           movie_api_configured=API_KEY is not None,
                           environment=os.getenv("ENVIRONMENT", "development")
                           )# renders status and passes all these variables

def insert_movie(data):
    conn = get_conn()#tries to connect to db
    if conn is None:
        return False
    try:
        with conn:
            with conn.cursor() as cur:
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
                ))#uses %s as opposed to ? as it is psycopg3, inserts the data into the supabase database, called unnormalised_movie as table is unnormalised
        cache.delete('movies')# ends the movie cache to prevent stale data
    except Exception:
        return False
@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    conn = get_conn()# connects to db
    if conn is None:
        flash("Database is down! action can not be completed.","error")
        return redirect(url_for("view"))# returns error message is no connection established, no actions can be completed on the backup database to preserve consistency
    with conn: # with conn seems to be a bit more elegant than others methods, you don't have to close the connection either
        with conn.cursor() as cur:
            cur.execute("DELETE FROM unnormalised_movie WHERE id = %s", (movie_id,)) #deletes the selected movie
    cache.delete('movies')# ends the movie cache to prevent stale data
    return redirect(url_for('view'))
@app.route('/view/')
def view():
    cached = cache.get('movies')# looks for a cache of movie, this speeds up loading time
    if cached:
        return render_template("view.html", unnormalised_movie=cached)
    conn = get_conn()# connects to db
    if conn is None:
        movies = load_movies_from_local()
        flash('Database is currently down, backup is available','error')
        return render_template("view.html", unnormalised_movie=movies)# if no connection established, backup db is used to display movies
    with conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('SELECT * FROM unnormalised_movie')
            unnormalised_movie = cur.fetchall()
    cache.set('movies', unnormalised_movie)
    save_movies_to_local(unnormalised_movie)
    return render_template('view.html', unnormalised_movie=unnormalised_movie)# if connection is established to supabase db displays all entries

def movie_exists(title):
    conn = get_conn()
    if conn is None:
        return False
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM unnormalised_movie WHERE movie_title ILIKE %s", (title,))# searches within the db for movies with the same name that you've entered
                return cur.fetchone() is not None# allows the movie to be saved only if not already present
    except Exception:
        return False
if __name__ == "__main__":
    app.run(debug=True)