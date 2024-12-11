from flask import Blueprint, request, jsonify
from app.models import db, Account, Income, Expense
from marshmallow import Schema, fields, ValidationError

from app.schemas import AccountSchema

# Blueprint для акаунтів
account_bp = Blueprint('accounts', __name__)

account_schema = AccountSchema()

@account_bp.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    try:
        validated_data = account_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

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
def get_account(user_id):
    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        return jsonify({"message": "Account not found"}), 404

    return jsonify({
        "account_id": account.id,
        "user_id": account.user_id,
        "balance": account.balance
    })

@account_bp.route("/accounts/<int:user_id>", methods=['DELETE'])
def delete_account(user_id):
    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        return jsonify({"message": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 200