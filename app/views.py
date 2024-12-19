from flask import request, jsonify, Blueprint
from datetime import datetime

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from app import Database as old_db
from app.models import User, db
from app.schemas import UserSchema, CategorySchema, RecordSchema
from marshmallow import ValidationError

lab2_bp = Blueprint('lab2', __name__)

user_schema = UserSchema()
category_schema = CategorySchema()
record_schema = RecordSchema()

@lab2_bp.route("/healthcheck")
def healthcheck():
    return jsonify(datetime.today(), "Service status: OK"), 200

def generate_id(data_dict):
    return max(data_dict.keys(), default=0) + 1

# Routes for User
@lab2_bp.route("/user/register", methods=['POST'])
def register_user():
    user_data = request.get_json()
    err = user_schema.validate(user_data)
    if err:
        return jsonify(err), 400

    user = User(
        username=user_data["username"],
        password=pbkdf2_sha256.hash(user_data["password"])
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exists"}), 400

    response = {
        "id": user.id,
        "message": "User registered",
        "date": datetime.today(),
    }
    return jsonify(response), 201

@lab2_bp.route('/user/login', methods=['POST'])
def login():
    user_data = request.get_json()
    username = user_data["username"]
    password = user_data["password"]

    user = User.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token,
                        "user_id": user.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@lab2_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user_schema.dump(user)), 200

@lab2_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

@lab2_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True)), 200

# Routes for Category
@lab2_bp.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(old_db.categories.values()))

@lab2_bp.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        validated_data = category_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    category_id = generate_id(old_db.categories)
    old_db.categories[category_id] = {'id': category_id, 'name': data['name']}
    return jsonify(old_db.categories[category_id])

@lab2_bp.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id in old_db.categories:
        del old_db.categories[category_id]
        return jsonify({'message': 'Category deleted successfully'})
    return jsonify({'error': 'Category not found'}), 404

# Routes for Record
@lab2_bp.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = old_db.records.get(record_id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    return jsonify(record)

@lab2_bp.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id in old_db.records:
        del old_db.records[record_id]
        return jsonify({'message': 'Record deleted successfully'})
    return jsonify({'error': 'Record not found'}), 404

@lab2_bp.route('/record', methods=['POST'])
def create_record():
    data = request.get_json()
    try:
        validated_data = record_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    record_id = generate_id(old_db.records)
    old_db.records[record_id] = {
        'id': record_id,
        'user_id': data['user_id'],
        'category_id': data['category_id'],
        'timestamp': datetime.today(),
        'amount': data['amount']
    }
    return jsonify(old_db.records[record_id])

@lab2_bp.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({'error': 'Please provide user_id or category_id or both'}), 400

    filtered_records = [
        record for record in old_db.records.values()
        if (not user_id or record['user_id'] == int(user_id)) and
           (not category_id or record['category_id'] == int(category_id))
    ]
    return jsonify(filtered_records)
