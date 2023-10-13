from flask_restful import Resource
from flask import request, make_response

from service import get_all_users


class Users(Resource):

    def get(self):
        token = request.headers.get('Authorization')

        result = get_all_users(token)
        return make_response(result)
