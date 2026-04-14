import pytest # setting up pytest
from app import app # from app.py

# Set up a test client to make faake HTTP requests
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Check ready responds with 200 (healthy) or 500 (unhealthy)
def test_health_endpoint_reports_dependencies(client):
    response = client.get('/ready')
    assert response.status_code in [200, 500] # response
    assert response.status_code in [200, 500]

# status page loads successfully
def test_expected_fields_are_going_to_be_returned_successfully(client):
    response = client.get('/status')
    assert response.status_code == 200

# home page loads successfully
def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200

# index page loads successfully
def test_index_page_loads(client):
    response = client.get('/index/')
    assert response.status_code == 200

# view page loads successfully
def test_view_page_loads(client):
    response = client.get('/view/')
    assert response.status_code == 200

# status page loads successfully
def test_status_page_loads(client):
    response = client.get('/status')
    assert response.status_code == 200