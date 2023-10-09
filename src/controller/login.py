import jwt
import bcrypt

from flask_restful import Resource
from flask import jsonify, request, make_response
from datetime import datetime, timedelta, date

from os import environ
from connection import cur


class Login(Resource):
    def post(self):
        data_json = request.json
        user = data_json["user"]
        passwd = data_json["passwd"]
        
        hash = cur.execute(f'''SELECT passwd FROM user WHERE user = "{user}"''')
        print(hash)

        if bcrypt.hashpw(passwd.encode('utf-8'), hash.encode('utf-8')) == hash.encode('utf-8'):
            payload = {
                "username": user,
                "exp": datetime.utcnow() + timedelta(hours=1000)
            }
            secret_key = environ["SECRET_KEY"]
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            date_now = date.today()

            cur.execute(f'''INSERT INTO token (token, expiration_date) 
            VALUES("{token}", "{date_now}");''')

            response = jsonify({"message" : "Ok"})
            response.status_code = 200
            return make_response(response)