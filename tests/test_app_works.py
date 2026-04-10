import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint_reports_dependencies(client):
    response = client.get('/ready')
    assert response.status_code in [200, 500]
    assert 'status' in response.json

def test_expected_fields_are_going_to_be_returned_successfully(client):
    response = client.get('/status')
    assert response.status_code == 200
    assert 'database' in response.json
    assert 'movie_api_configured' in response.json
    assert 'environment' in response.json