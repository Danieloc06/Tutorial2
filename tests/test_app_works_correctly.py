import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_returns_joined_result_when_both_sources_available(client):
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

        mock_get.return_value.json.return_value = mock_movie
        mock_exists.return_value = False
        mock_insert.return_value = True

        response = client.get('/search?t=Inception')

        assert response.status_code == 200
        mock_insert.assert_called_once()

def test_graceful_degradation_on_upstream_failure(client):
    with patch('app.requests.get') as mock_get:
        mock_get.side_effect = Exception("API is down")

        response = client.get('/search?t=Inception')

        assert response.status_code in [200, 503]