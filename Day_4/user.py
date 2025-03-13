from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
users_file = 'users.json'

def read_users():
    if not os.path.exists(users_file):
        return []
    with open(users_file, 'r') as file:
        return json.load(file)

def write_users(users):
    with open(users_file, 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/users', methods=['GET'])
def get_users():
    users = read_users()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    users = read_users()
    users.append(new_user)
    write_users(users)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user = request.json
    users = read_users()
    for user in users:
        if user['user_id'] == user_id:
            user.update(updated_user)
            write_users(users)
            return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = read_users()
    users = [user for user in users if user['user_id'] != user_id]
    write_users(users)
    return jsonify({'message': 'User deleted'})

if __name__ == '__main__':
    app.run(debug=True)
