import pytest
from unittest.mock import patch
from app import app

# Set up a test client to make fake HTTP requests
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Check that searching for a movie saves it to the database successfully
def test_returns_joined_result_when_both_sources_available(client):
# Inputting a movie that can test if it saves successfully
    mock_movie = {
        "Response": "True",
        "Title": "Inception",
        "Year": "2010",
        "Rated": "PG-13",
        "Released": "16 Jul 2010",
        "Runtime": "148 min",
        "Genre": "Action",
        "Director": "Nolan",
        "Writer": "Nolan",
        "Actors": "DiCaprio",
        "Plot": "Dreams",
        "Poster": "url",
        "imdbRating": "8.8",
        "imdbID": "tt1375666",
        "BoxOffice": "$292M"
    }
    with patch('app.requests.get') as mock_get, \
         patch('app.movie_exists') as mock_exists, \
         patch('app.insert_movie') as mock_insert:

        mock_get.return_value.json.return_value = mock_movie # Fake API returns our movie example
        mock_exists.return_value = False
        mock_insert.return_value = True # saving movie correctly

        response = client.get('/search?t=Inception')

        assert response.status_code == 200 # Page should load successfully
        mock_insert.assert_called_once()

# Check that the app handles a failing API gracefully without crashing
def test_graceful_degradation_on_upstream_failure(client):
    with patch('app.requests.get') as mock_get:
        mock_get.side_effect = Exception("API is down")

        response = client.get('/search?t=Inception')

        assert response.status_code in [200, 503] # Should handle the failure gracefully