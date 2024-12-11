from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=True)

    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)

    # Реєстрація Blueprints
    from app.routes import income_routes
    app.register_blueprint(income_routes.income_bp)
    from app.routes import expense_routes
    app.register_blueprint(expense_routes.expense_bp)
    from app.routes import account_routes
    app.register_blueprint(account_routes.account_bp)
    from app import views
    app.register_blueprint(views.lab2_bp)

    return app