from flask_restful import Resource
from flask import request, make_response

from service import verify_info_on_db


class VerifyUserEmail(Resource):
    def post(self, info):
        data_json = request.json

        response = verify_info_on_db(info, data_json)
        return make_response(response)
