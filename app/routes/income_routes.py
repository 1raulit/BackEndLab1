from flask import Blueprint, request, jsonify
from app.models import db, Account, Income
from app.schemas import IncomeSchema
from marshmallow import ValidationError

income_bp = Blueprint('income', __name__)
income_schema = IncomeSchema()

@income_bp.route('/accounts/<int:user_id>/income', methods=['POST'])
def add_income(user_id):
    data = request.get_json()
    try:
        validated_data = income_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    account = Account.query.filter_by(user_id=user_id).first()
    if not account:
        return jsonify({"message": "Account not found"}), 404
    income = Income(
        account_id=account.id,
        amount=validated_data['amount'],
        description=validated_data['description'],
        date=validated_data['date']
    )
    account.balance += income.amount

    db.session.add(income)
    db.session.commit()
    return jsonify({"message": "Income added", "balance": account.balance}), 201
