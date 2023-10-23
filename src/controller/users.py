from flask_restful import Resource
from flask import make_response

from service import get_all_users


class Users(Resource):
    def get(self):
        result = get_all_users()
        return make_response(result)
 