from os import environ
from datetime import datetime, timedelta

import jwt
import bcrypt

from connection import cur, conn
from storage import insert_token, select_token_by_user, select_passwd_id
from utils import return_response, verify_none_values_json


def login(data_json):
    null_on_data = verify_none_values_json(data_json)
    if null_on_data is False:
        user = data_json["user"]
        passwd = data_json["passwd"]

        select_passwd_id(user)
        result = cur.fetchone()
        if result:
            hash_value = str(result[0])
            id_user = result[1]
        else:
            return return_response(404, "Not found")

        if bcrypt.checkpw(passwd.encode("utf-8"), hash_value.encode("utf-8")):
            select_token_by_user(user)
            result = cur.fetchone()
            if result:
                token = result[0]
                return token

            payload = {
                "username": user,
                "exp": datetime.utcnow() + timedelta(hours=500),
            }
            secret_key = environ["SECRET_KEY"]
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            date_exp = payload["exp"]

            conn.begin()
            insert_token(id_user, token, date_exp)
            rows_affected = cur.rowcount
            conn.commit()

            if rows_affected == 0:
                return return_response(204, "No rows affected")

            return token
        return return_response(401, "Wrong password")
    return null_on_data
 