import sqlite3
import json
from flask_caching import Cache

cache = Cache()

def init_cache(app):
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})

def save_movies_to_local(movies):
    conn = sqlite3.connect('local_cache.db')#Open a connection to the database
    conn.execute('''CREATE TABLE IF NOT EXISTS unnormalised_movie 
                    (id INTEGER PRIMARY KEY, data TEXT)''') # Creating the table if it does not exist
    for movie in movies:
        conn.execute('INSERT OR REPLACE INTO unnormalised_movie (id, data) VALUES (?, ?)',
                     (movie['id'], json.dumps(movie, default=str))) #Insert the move
    conn.commit()
    conn.close()

def load_movies_from_local():
    try:
        conn = sqlite3.connect('local_cache.db') #Open connection to the database
        rows = conn.execute('SELECT data FROM unnormalised_movie').fetchall() #Fetching all of the movie data
        conn.close()
        return [json.loads(row[0]) for row in rows]
    except Exception:
        return [] #If anything happens return an empty list