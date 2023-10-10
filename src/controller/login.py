import jwt
import bcrypt

from flask_restful import Resource
from flask import jsonify, request, make_response
from datetime import datetime, timedelta, date

from os import environ
from connection import cur, connection


class Login(Resource):
    def post(self):
        data_json = request.json
        user = data_json["user"]
        passwd = data_json["passwd"]
        
        cur.execute(f'SELECT passwd FROM user WHERE user = "{user}"')
        result = cur.fetchone()
        if result:
            hash = str(result[0])
        else:
            response = jsonify({"message" : "Not found"})
            response.status_code = 404
            return make_response(response)

        if bcrypt.checkpw(passwd.encode('utf-8'), hash.encode('utf-8')):
            payload = {
                "username": user,
                "exp": datetime.utcnow() + timedelta(hours=1000)
            }
            secret_key = environ["SECRET_KEY"]
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            date_exp = payload["exp"]

            cur.execute(f'''INSERT INTO token (id, token, expiration_date)
                VALUES ((SELECT id FROM user WHERE user = "{user}"), "{token}", "{date_exp}");''')
            connection.commit()

            response = jsonify({"message" : "Ok"})
            response.status_code = 200
            return make_response(response)
