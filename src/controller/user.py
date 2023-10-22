from flask_restful import Resource
from flask import request, make_response

from service import get_user_by_token, register_user, update_user, delete_user


class User(Resource):
    def get(self):
        token = request.headers.get("authorization")

        result = get_user_by_token(token)
        return make_response(result)

    def post(self):
        data_json = request.json

        response = register_user(data_json)
        return make_response(response)

    def put(self):
        token = request.headers.get("authorization")
        data_json = request.json

        response = update_user(token, data_json)
        return response

    def delete(self):
        token = request.headers.get("authorization")

        response = delete_user(token)
        return response
