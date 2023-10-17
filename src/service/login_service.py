from os import environ
from datetime import datetime, timedelta

import jwt
import bcrypt

from connection import cur, connection
from storage import select_passwd_id, insert_token
from utils import return_response


def login(data_json):
    if data_json == None:
        return return_response(401, "Unauthorized")
    
    user = data_json["user"]
    passwd = data_json["passwd"]

    select_passwd_id(user)
    result = cur.fetchone()
    if result:
        hash = str(result[0])
        id_user = result[1]
    else:
        return return_response(404, "Not found")

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

        return return_response(200, "Ok")
