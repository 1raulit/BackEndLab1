from flask import request, jsonify, Blueprint
from datetime import datetime
from app import Database as db
from app.schemas import UserSchema, CategorySchema, RecordSchema
from marshmallow import ValidationError

lab2_bp = Blueprint('lab2', __name__)

user_schema = UserSchema()
category_schema = CategorySchema()
record_schema = RecordSchema()

@lab2_bp.route("/healthcheck")
def healthcheck():
    return jsonify(datetime.today(), "Service status: OK"), 200

# Helper function to generate unique IDs
def generate_id(data_dict):
    return max(data_dict.keys(), default=0) + 1

# Routes for User
@lab2_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@lab2_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in db.users:
        del db.users[user_id]
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

@lab2_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        validated_data = user_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = generate_id(db.users)
    db.users[user_id] = {'id': user_id, 'name': data['name']}
    return jsonify(db.users[user_id])

@lab2_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(db.users.values()))

# Routes for Category
@lab2_bp.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(db.categories.values()))

@lab2_bp.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        validated_data = category_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    category_id = generate_id(db.categories)
    db.categories[category_id] = {'id': category_id, 'name': data['name']}
    return jsonify(db.categories[category_id])

@lab2_bp.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id in db.categories:
        del db.categories[category_id]
        return jsonify({'message': 'Category deleted successfully'})
    return jsonify({'error': 'Category not found'}), 404

# Routes for Record
@lab2_bp.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = db.records.get(record_id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    return jsonify(record)

@lab2_bp.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id in db.records:
        del db.records[record_id]
        return jsonify({'message': 'Record deleted successfully'})
    return jsonify({'error': 'Record not found'}), 404

@lab2_bp.route('/record', methods=['POST'])
def create_record():
    data = request.get_json()
    try:
        validated_data = record_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    record_id = generate_id(db.records)
    db.records[record_id] = {
        'id': record_id,
        'user_id': data['user_id'],
        'category_id': data['category_id'],
        'timestamp': datetime.today(),
        'amount': data['amount']
    }
    return jsonify(db.records[record_id])

@lab2_bp.route('/record', methods=['GET'])
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
