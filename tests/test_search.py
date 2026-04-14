import pytest # importing the pytest
from unittest.mock import patch
from app import app # app.py

# Set up a test client to make fake HTTP requests
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# The test should return 400 error if no title is provided
def test_search_returns_400_when_no_title(client):
    response = client.get('/search')
    assert response.status_code == 400
    assert 'error' in response.json

# The test should handle duplicate movie title correctly
def test_search_handles_duplicate_title(client):
    with patch('app.movie_exists') as mock_exists, \
         patch('app.insert_movie') as mock_insert:

        mock_exists.return_value = True # movie is already in existence

        response = client.get('/search?t=Inception')

        assert response.status_code == 200 # Request should still succeed
        mock_insert.assert_not_called()
