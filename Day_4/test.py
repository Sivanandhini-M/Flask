import pytest
from users import app, USER_FILE
import json
import os

@pytest.fixture
def client():
    with app.test_client() as client:
        # Prepare a clean test environment
        if os.path.exists(USER_FILE):
            os.remove(USER_FILE)
        yield client

def test_create_user(client):
    response = client.post('/users', json={
        "user_id": 1, 
        "user_name": "Alice", 
        "user_designation": "Developer"
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully!'

def test_get_users(client):
    client.post('/users', json={
        "user_id": 1, 
        "user_name": "Alice", 
        "user_designation": "Developer"
    })
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['user_name'] == 'Alice'

def test_update_user(client):
    client.post('/users', json={
        "user_id": 1, 
        "user_name": "Alice", 
        "user_designation": "Developer"
    })
    response = client.put('/users/1', json={
        "user_name": "Alice Smith", 
        "user_designation": "Senior Developer"
    })
    assert response.status_code == 200
    assert response.json['message'] == 'User updated successfully!'

def test_update_user_not_found(client):
    response = client.put('/users/999', json={
        "user_name": "Ghost", 
        "user_designation": "Unknown"
    })
    assert response.status_code == 404
    assert response.json['message'] == 'User not found!'

def test_delete_user(client):
    client.post('/users', json={
        "user_id": 1, 
        "user_name": "Alice", 
        "user_designation": "Developer"
    })
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json['message'] == 'User deleted successfully!'

def test_delete_user_not_found(client):
    response = client.delete('/users/999')
    assert response.status_code == 404
    assert response.json['message'] == 'User not found!'
