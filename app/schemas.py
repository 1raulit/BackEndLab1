from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    name = fields.String(required=True)

class CategorySchema(Schema):
    name = fields.String(required=True)

class RecordSchema(Schema):
    user_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    amount = fields.Integer(required=True)

class AccountSchema(Schema):
    user_id = fields.Integer(required=True)

class IncomeSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    description = fields.String(required=True, validate=validate.Length(min=3, max=255))
    date = fields.String(required=True)

class ExpenseSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    description = fields.String(required=True, validate=validate.Length(min=3, max=255))
    date = fields.String(required=True)