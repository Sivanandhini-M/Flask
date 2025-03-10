from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
USERS_FILE = 'users.json'

# Initialize the JSON file if it doesn't exist
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

def read_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def write_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/users', methods=['GET'])
def get_users():
    users = read_users()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    users = read_users()
    new_user['user_id'] = len(users) + 1
    users.append(new_user)
    write_users(users)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    users = read_users()
    user = next((user for user in users if user['user_id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    user['user_name'] = request.json.get('user_name', user['user_name'])
    user['user_designation'] = request.json.get('user_designation', user['user_designation'])
    write_users(users)
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = read_users()
    user = next((user for user in users if user['user_id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    users.remove(user)
    write_users(users)
    return jsonify({'message': 'User deleted'})

if __name__ == '__main__':
    app.run(debug=True)

filename = 'users.json'

#create_user(filename, user_name= "Jane black", user_designation= "Senior manager") 
update_user(filename, user_id = 4, user_name= "Jane white", user_designation= "Senior Developer")
#delete_user(filename, 3)
