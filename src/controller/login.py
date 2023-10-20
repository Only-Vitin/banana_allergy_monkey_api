from flask_restful import Resource
from flask import request, make_response, jsonify

from service import login


class Login(Resource):
    def post(self):
        data_json = request.json
        
        token = login(data_json)
        if type(token) == str:
            response = jsonify({"Authorization" : f"{token}"})
            return make_response(response)
        return make_response(token)
