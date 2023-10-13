from flask_restful import Resource
from flask import request, make_response

from service import login


class Login(Resource):
    def post(self):
        data_json = request.json
        
        response = login(data_json)

        return make_response(response)
