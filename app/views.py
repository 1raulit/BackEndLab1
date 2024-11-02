from flask import Flask, request, jsonify
from datetime import datetime
from Database import *

app = Flask(__name__)


@app.route("/healthcheck")
def healthcheck():
    return jsonify(datetime.today(), "Service status: OK"), 200

# Helper function to generate unique IDs
def generate_id(data_dict):
    return max(data_dict.keys(), default=0) + 1

# Routes for User
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = generate_id(users)
    users[user_id] = {'id': user_id, 'name': data['name']}
    return jsonify(users[user_id])

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))


# Run the application
if __name__ == '__main__':
    app.run(debug=False)
