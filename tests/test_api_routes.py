import pytest
from flask import Flask
from app import app  # Import your Flask app

# cmd: `pytest --cov=your_project tests/`

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_list_routes(client):
    response = client.get('/routes')
    assert response.status_code == 200
    assert b'routes' in response.data

def test_create_tag(client):
    response = client.post('/tags/', json={'name': 'test_tag'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'test_tag'

def test_get_tags(client):
    response = client.get('/tags/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
