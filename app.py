from datetime import timedelta

from elasticsearch import Elasticsearch
from flask import Flask
from flask_login import LoginManager
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
    return app, api


app, api = create_app()

app.config['SECRET_KEY'] = 'secretiveness404'
#app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
# app.config["SESSION_TYPE"] = "filesystem"
# app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'


from applications.controllers import *

from applications.api import *

if __name__ == '__main__':
    app.run()