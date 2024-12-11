import os

PROPAGATE_EXCEPTIONS = True
FLASK_DEBUG = True
SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["DB_HOST"]}/{os.environ["POSTGRES_DB"]}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
API_TITLE = "Finance REST API"
API_VERSION = "v1"