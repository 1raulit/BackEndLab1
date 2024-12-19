from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import db, Account, Income, Expense
from marshmallow import Schema, fields, ValidationError

from app.schemas import AccountSchema

# Blueprint для акаунтів
account_bp = Blueprint('accounts', __name__)

account_schema = AccountSchema()

@account_bp.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
    data = request.get_json()
    try:
        validated_data = account_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    current_user_id = int(get_jwt_identity())
    if current_user_id != data["user_id"]:
        return jsonify({"message": "Access denied"}), 403

    account = Account.query.filter_by(user_id=validated_data['user_id']).first()
    if account:
        return jsonify({"message": "Account with this user_id already created"}), 400

    # Створюємо новий акаунт
    account = Account(user_id=validated_data['user_id'], balance=0.0)
    db.session.add(account)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully",
        "account_id": account.id,
        "user_id": account.user_id,
        "balance": account.balance
    }), 201

@account_bp.route('/accounts/<int:user_id>', methods=['GET'])
@jwt_required()
def get_account(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Access denied"}), 403

    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        return jsonify({"message": "Account not found"}), 404

    return jsonify({
        "account_id": account.id,
        "user_id": account.user_id,
        "balance": account.balance
    })

@account_bp.route("/accounts/<int:user_id>", methods=['DELETE'])
@jwt_required()
def delete_account(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Access denied"}), 403

    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        return jsonify({"message": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 200