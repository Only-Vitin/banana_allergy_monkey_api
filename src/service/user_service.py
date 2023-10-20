from datetime import date

from flask import jsonify
import bcrypt

from connection import cur, connection
from utils import query_to_json, valid_token, return_response, verify_none_values_json
from storage import select_user_by_token, insert_user, update_register_by_token, delete_register_by_id, select_id_by_token


def get_user_by_token(token):
    response = valid_token(token)
    if response.get_json()["message"] == "Ok":
        select_user_by_token(token)

        columns = [x[0] for x in cur.description]
        lines = cur.fetchall()

        result = query_to_json(columns, lines)
        result_json = jsonify(result)
        result_json.status_code = 200
        return result_json
    return response


def register_user(data_json):
    null_on_data = verify_none_values_json(data_json)
    if null_on_data == False:
        passwd = data_json["passwd"]
        hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
        data_json["passwd"] = hash.decode('utf-8')

        date_now = date.today()
        
        connection.begin()
        insert_user(data_json["user"], data_json["email"], data_json["name"], data_json["passwd"], date_now)
        connection.commit()

        return return_response(201, "Created")
    return null_on_data

def update_user(token, data_json):
    null_on_data = verify_none_values_json(data_json)
    if null_on_data == False:
        response = valid_token(token)
        if response.get_json()["message"] == "Ok":
            passwd = data_json["passwd"]
            hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
            data_json["passwd"] = hash.decode('utf-8')

            date_now = date.today()

            connection.begin()
            update_register_by_token(token, data_json["user"], data_json["name"], data_json["email"], data_json["passwd"], date_now)
            connection.commit()

            return response
        return response
    return null_on_data

def delete_user(token):
    response = valid_token(token)

    if response.get_json()["message"] == "Ok":
        select_id_by_token(token)
        result = cur.fetchone()

        if result:
            id_user = result[0]
        else:
            return return_response(404, "Not found")

        connection.begin()
        delete_register_by_id(id_user)
        connection.commit()

        return response
    return response