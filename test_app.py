import pytest
from app import app  # Import your Flask app from the app.py


# Pytest fixture to initialize the test client
@pytest.fixture
def client():
    with app.test_client() as client:
        app.config['TESTING'] = True
        yield client

# Test the homepage renders correctly
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200  # Check if the status code is 200
    assert b'Image Scraper' in response.data