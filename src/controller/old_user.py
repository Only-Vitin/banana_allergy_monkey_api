import jwt
import bcrypt
import pandas as pd

from datetime import datetime, timedelta

from flask_restful import Resource
from flask import jsonify, request, make_response

from os import environ
from connection import connection

class User(Resource):
    def get(self):
        try:
            register_df = pd.read_sql_table(environ["TABLE_REGISTER"], connection)
            user = request.args.get("user")
            result = register_df.query("@user in user")

            if result.empty:
                return make_response(jsonify({"message": f"Usuário '{user}' não encontrado"}), 404)
            else:
                result_dict = result.to_dict(orient="records")
        except KeyError as e:
            if "boolean index" in str(e):
                return make_response(jsonify({"message": "Verifique os parâmetros"}), 400)
        else:
            return make_response(jsonify(result_dict))

    def post(self):
        data_json = request.json
        user = data_json["user"]
        passwd = data_json["passwd"]
        passwd = passwd.encode('utf-8')
        
        hash = bcrypt.hashpw(passwd, bcrypt.gensalt())
        data_json["passwd"] = hash

        if bcrypt.hashpw(passwd.encode('utf-8'), hash.encode('utf-8')) == hash.encode('utf-8'):
            payload = {
                "username": user,
                "exp": datetime.utcnow() + timedelta(hours=1000)
            }
            secret_key = environ["SECRET_KEY"]
            token = jwt.encode(payload, secret_key, algorithm="HS256")

        data_json["token"] = token

        register_df = pd.read_sql_table(environ["TABLE_REGISTER"], connection)
        data_df = pd.DataFrame([data_json])
        register_df = pd.concat([register_df, data_df], ignore_index=True)
        
        register_df.to_sql(environ["TABLE_REGISTER"], connection, if_exists="replace", index=False)
        return make_response(jsonify({"message": "Usuário cadastrado com sucesso"}), 200)
