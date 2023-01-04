from flask import Flask
from flask_restful import Resource, Api
from applications.database import db
from applications.config import LocalDevelopmentConfig
from applications.models import *

app = None
api = None


def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app,api


app,api = create_app()

app.config['SECRET_KEY'] = '84da5b8a39a6d06bf8bc7a60cedcac93'

from applications.controllers import *

from applications.api import *
api.add_resource(UserAPI, "/api/userinfo", "/api/userinfo/<string:username>")

if __name__ == '__main__':
    app.run()
