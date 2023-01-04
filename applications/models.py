from flask_login import UserMixin
from .database import db
from flask import current_app as app


class Userinfo(db.Model):
    __tablename__ = 'userinfo'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String, unique=True, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


