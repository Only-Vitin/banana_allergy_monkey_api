from datetime import date

from flask import jsonify
import bcrypt

from connection import cur, connection
from utils import query_to_json, valid_token, return_response
from storage import select_user_by_token, insert_user, update_register_by_token


def get_user_by_token(token):
    if token:
        select_user_by_token(token)
    else:
        return return_response(401, "Unauthorized")

    columns = [x[0] for x in cur.description]
    lines = cur.fetchall()

    result = query_to_json(columns, lines)
    result_json = jsonify(result)
    result_json.status_code = 200
    return result_json


def register_user(data_json):
    if data_json == None:
        return return_response(401, "Unauthorized")

    passwd = data_json["passwd"]
    hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
    data_json["passwd"] = hash.decode('utf-8')

    date_now = date.today()
    
    connection.begin()
    insert_user(data_json["user"], data_json["email"], data_json["name"], data_json["passwd"], date_now)
    connection.commit()

    return return_response(201, "Created")

def update_user(token, data_json):
    response = valid_token(token)

    passwd = data_json["passwd"]
    hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
    data_json["passwd"] = hash.decode('utf-8')

    date_now = date.today()

    connection.begin()
    update_register_by_token(token, data_json["user"], data_json["name"], data_json["email"], data_json["passwd"], date_now)
    connection.commit()
    
    return return_response(200, "Ok")