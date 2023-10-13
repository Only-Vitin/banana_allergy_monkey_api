from os import environ
from datetime import datetime, timedelta

import jwt
import bcrypt
from flask import jsonify

from connection import cur, connection
from storage import select_passwd_id, insert_token


def login(data_json):
    if data_json == None:
        response = jsonify({"message" : "Unauthorized"})
        response.status_code = 401
        return response
    
    user = data_json["user"]
    passwd = data_json["passwd"]

    select_passwd_id(user)
    result = cur.fetchone()
    if result:
        hash = str(result[0])
        id_user = result[1]
    else:
        response = jsonify({"message" : "Not found"})
        response.status_code = 404
        return response

    if bcrypt.checkpw(passwd.encode('utf-8'), hash.encode('utf-8')):
        payload = {
            "username": user,
            "exp": datetime.utcnow() + timedelta(hours=1000)
        }
        secret_key = environ["SECRET_KEY"]
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        date_exp = payload["exp"]

        connection.begin()
        insert_token(id_user, token, date_exp)
        connection.commit()

        response = jsonify({"message" : "Ok"})
        response.status_code = 200
        return response
