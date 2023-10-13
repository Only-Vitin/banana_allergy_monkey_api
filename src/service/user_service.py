from datetime import date

import bcrypt
from flask import jsonify

from connection import cur, connection
from storage import select_user_by_token, insert_user
from utils import query_to_json


def get_user_by_token(token):
    if token:
        select_user_by_token(token)
    else:
        response = jsonify({"message" : "Unauthorized"})
        response.status_code = 401
        return response

    columns = [x[0] for x in cur.description]
    lines = cur.fetchall()

    result = query_to_json(columns, lines)
    result_json = jsonify(result)
    result_json.status_code = 200
    return result_json


def register_user(data_json):
    if data_json == None:
        response = jsonify({"message" : "Unauthorized"})
        response.status_code = 401
        return response

    passwd = data_json["passwd"]
    
    hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
    data_json["passwd"] = hash.decode('utf-8')

    date_now = date.today()
    
    connection.begin()
    insert_user(data_json["user"], data_json["email"], data_json["name"], data_json["passwd"], date_now)
    connection.commit()

    response = jsonify({"message" : "Created"})
    response.status_code = 201
    return response
