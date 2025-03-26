from flask import Flask, request, jsonify
import json
import pytest
from users import app
from users import load_users
app.load_users = load_users


@pytest.fixture

def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user_success(client):
    user = {
        "user_id": 1,
        "user_name": "John",
        "user_designation": "Manager"
    }
    response = client.post('/users', json=user)
    assert response.status_code == 201
    assert response.json == {"message": "User created successfully"}

def test_get_users():
    with app.app_context():
        try:
            users = app.load_users()
            return jsonify(users), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


def validate_user(data):
    if not isinstance(data, dict):
        return "Invalid payload format"
    if 'user_id' not in data or 'user_name' not in data or 'user_designation' not in data:
        return "Invalid JSON structure"
    if not isinstance(data['user_id'], int) or data['user_id'] <= 0:
        return "Invalid user_id"
    if not isinstance(data['user_name'], str) or not data['user_name'].strip() or not data['user_name'].isalpha():
        return "Invalid or empty user_name"
    if not isinstance(data['user_designation'], str) or not data['user_designation'].strip() or not data['user_designation'].isalpha():
        return "Invalid or empty user_designation"
    return None


def update_user(user_id):
    try:
        user_data = request.get_json()
        error = validate_user(user_data)
        if error:
            return jsonify({"error": error}), 400

        users = app.load_users()
        user = next((u for u in users if u['user_id'] == user_id), None)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.update(user_data)
        app.save_users(users)
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def test_delete_user():
    user_id = 1 
    with app.test_request_context():
        users = app.load_users()
    user = next((u for u in users if u['user_id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users.remove(user)
    app.save_users(users)
    return jsonify({"message": "User deleted successfully"}), 200
    
        




