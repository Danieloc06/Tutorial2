import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_deletion_works(client):
    with patch('app.get_conn') as mock_conn, \
         patch('app.cache'):


        response = client.post('/delete_movie/1')

        assert response.status_code == 302