import config

from flask import Flask
from sqlalchemy import create_engine

from model.user_dao import UserDao
from service import UserService
from views import create_endpoints


class Services:
    pass


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    print(app.config['DB_URL'])
    database = create_engine("postgresql://postgres:0399@localhost:5432/internproject")

    user_dao = UserDao(database)

    services = Services
    services.user_service = UserService(user_dao, config)

    create_endpoints(app, services)

    return app