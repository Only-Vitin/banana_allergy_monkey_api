import bcrypt
import pandas as pd

from flask_restful import Resource
from flask import jsonify, request, make_response

from os import environ
from connection import connection


class VerificaLogin(Resource):
    def get(self):
        data_json = request.json
        register_df = pd.read_sql_table(environ["TABLE_REGISTER"], connection)
        user = data_json["user"]
        passwd = data_json["passwd"]

        result = register_df.query("@user in user")

        if result.empty:
            return None
        else:
            hash = result.iloc[0, 3]
            print(hash)
            if bcrypt.hashpw(passwd.encode('utf-8'), hash.encode('utf-8')) == hash.encode('utf-8'):
                return make_response(jsonify({"token": result['token']}))
            return None
