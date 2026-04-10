import pytest
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