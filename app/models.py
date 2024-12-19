from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Float, default=0.0)
    expenses = db.relationship('Expense', back_populates='account', cascade="all, delete-orphan", passive_deletes=True)

class Income(db.Model):
    __tablename__ = 'incomes'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    account = db.relationship('Account', back_populates='expenses')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
