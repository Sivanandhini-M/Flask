from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
USER_DATA_FILE = 'users.json'        

def read_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file: 
            return json.load(file)
    return []

# Helper function to write user data to the JSON file      
def write_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Create a user
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    users = read_user_data()
    new_user['user_id'] = len(users) + 1
    users.append(new_user)
    write_user_data(users)
    return jsonify(new_user), 201

# Get the list of users
@app.route('/users', methods=['GET'])
def get_users():
    users = read_user_data()
    return jsonify(users), 200

# Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    users = read_user_data()
    for user in users:
        if user['user_id'] == user_id:
            user.update(request.json)
            write_user_data(users)
            return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = read_user_data()
    users = [user for user in users if user['user_id'] != user_id]
    write_user_data(users)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
