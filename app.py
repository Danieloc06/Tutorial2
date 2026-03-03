import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# 1. Initialize the Flask app
app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")


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
if __name__ == "__main__":
    app.run(debug=True)