from flask_restful import Resource
from applications.database import db
from applications.models import *


class UserAPI(Resource):
    def get(self, username):
        """
        Get a user
        ---
        """
        userinfo = db.session.query(Userinfo).filter(Userinfo.username == username).first()

        if userinfo:
            return {"user_id": userinfo.user_id, "username": userinfo.username}
        else:
            return {}, 404

    def put(self):
        """
        Update a user
        ---
        """

    def delete(self):
        """
        Delete a user
        ---
        """

    def post(self):
        """
        Create a user
        ---
        """