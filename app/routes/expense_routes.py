from flask import Blueprint, request, jsonify
from app.models import db, Account, Expense
from app.schemas import ExpenseSchema
from marshmallow import ValidationError

expense_bp = Blueprint('expenses', __name__)
expense_schema = ExpenseSchema()

@expense_bp.route('/accounts/<int:user_id>/expenses', methods=['POST'])
def create_expense(user_id):
    data = request.get_json()
    try:
        validated_data = expense_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    account = Account.query.filter_by(user_id=user_id).first()

    # Перевіряємо баланс
    if account.balance < validated_data['amount']:
        return jsonify({"error": "Insufficient funds"}), 400

    # Створюємо витрату і списуємо кошти
    expense = Expense(
        account_id=account.id,
        amount=validated_data['amount'],
        description=validated_data['description'],
        date=validated_data['date']
    )
    account.balance -= validated_data['amount']

    db.session.add(expense)
    db.session.commit()

    return jsonify({"message": "Expense created", "balance": account.balance}), 201