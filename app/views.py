from flask import request, jsonify
from datetime import datetime
from app import Database as db
from app import app

@app.route("/healthcheck")
def healthcheck():
    return jsonify(datetime.today(), "Service status: OK"), 200

# Helper function to generate unique IDs
def generate_id(data_dict):
    return max(data_dict.keys(), default=0) + 1

# Routes for User
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in db.users:
        del db.users[user_id]
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = generate_id(db.users)
    db.users[user_id] = {'id': user_id, 'name': data['name']}
    return jsonify(db.users[user_id])

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(db.users.values()))

# Routes for Category
@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(db.categories.values()))

@app.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    category_id = generate_id(db.categories)
    db.categories[category_id] = {'id': category_id, 'name': data['name']}
    return jsonify(db.categories[category_id])

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id in db.categories:
        del db.categories[category_id]
        return jsonify({'message': 'Category deleted successfully'})
    return jsonify({'error': 'Category not found'}), 404

# Routes for Record
@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = db.records.get(record_id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    return jsonify(record)

@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id in db.records:
        del db.records[record_id]
        return jsonify({'message': 'Record deleted successfully'})
    return jsonify({'error': 'Record not found'}), 404

@app.route('/record', methods=['POST'])
def create_record():
    data = request.get_json()
    record_id = generate_id(db.records)
    db.records[record_id] = {
        'id': record_id,
        'user_id': data['user_id'],
        'category_id': data['category_id'],
        'timestamp': datetime.today(),
        'amount': data['amount']
    }
    return jsonify(db.records[record_id])

@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({'error': 'Please provide user_id or category_id or both'}), 400

    filtered_records = [
        record for record in db.records.values()
        if (not user_id or record['user_id'] == int(user_id)) and
           (not category_id or record['category_id'] == int(category_id))
    ]
    return jsonify(filtered_records)
