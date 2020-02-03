from os import environ, os
from flask_dotenv import DotEnv


class Config:
    """Set Flask configuration vars from .env file."""

    # General
    TESTING = environ.get('TESTING', True)
    FLASK_DEBUG = environ.get('FLASK_DEBUG', 1)
    SECRET_KEY = environ.get('SECRET_KEY', 'some-secret-key')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI', 'mysql://root:ledinek@localhost/used_cars_dealership')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # @classmethod
    # def init_app(self, app):
    #     env = DotEnv()
    #     env.init_app(app)