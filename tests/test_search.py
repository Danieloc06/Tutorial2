import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_returns_400_when_no_title(client):
    response = client.get('/search')
    assert response.status_code == 400
    assert 'error' in response.json

def test_search_handles_duplicate_title(client):
    with patch('app.movie_exists') as mock_exists, \
         patch('app.insert_movie') as mock_insert:

        mock_exists.return_value = True

        response = client.get('/search?t=Inception')

        assert response.status_code == 200
        mock_insert.assert_not_called()
