import pytest
from unittest.mock import patch
from app import app

# Set up a test client to make fake HTTP requests
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Checking when deleting a movie that the user is correctly redirected when the movie is deleted
def test_deletion_works(client):
    with patch('app.get_conn') as mock_conn, \
         patch('app.cache'):


        response = client.post('/delete_movie/1')

        assert response.status_code == 302 # 302 means redirect, expected after a successful delete