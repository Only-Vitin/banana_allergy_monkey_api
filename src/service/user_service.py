from datetime import date

from flask import jsonify
import bcrypt

from connection import cur, conn
from utils import query_to_json, valid_token, return_response, verify_none_values_json
from service.verify_user_email_service import verify_info_on_db
from storage import select_user_by_token, select_id_by_token
from storage import insert_user, update_register_by_token, delete_register_by_id


def get_user_by_token(token):
    response = valid_token(token)
    if response.get_json()["message"] == "Ok":
        select_user_by_token(token)
        rows_affected = cur.rowcount
        if rows_affected == 0:
            return return_response(204, "No rows affected")

        columns = [x[0] for x in cur.description]
        lines = cur.fetchall()

        result = query_to_json(columns, lines)
        result_json = jsonify(result)
        result_json.status_code = 200
        return result_json
    return response


def register_user(data_json):
    null_on_data = verify_none_values_json(data_json)
    if null_on_data is False:
        for validation in ["user", "email"]:
            response = verify_info_on_db(validation, data_json)
            if response.get_json()["message"] == "Already registered":
                return return_response(409, "Already registered")

        passwd = data_json["passwd"]
        hash_value = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())
        data_json["passwd"] = hash_value.decode("utf-8")

        date_now = date.today()

        conn.begin()
        insert_user(
            data_json["user"],
            data_json["email"],
            data_json["name"],
            data_json["passwd"],
            date_now,
        )
        rows_affected = cur.rowcount
        conn.commit()

        if rows_affected == 0:
            return return_response(204, "No rows affected")
        return return_response(201, "Created")
    return null_on_data


def update_user(token, data_json):
    null_on_data = verify_none_values_json(data_json)
    if null_on_data is False:
        response = valid_token(token)
        if response.get_json()["message"] == "Ok":
            passwd = data_json["passwd"]
            hash_value = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())
            data_json["passwd"] = hash_value.decode("utf-8")

            date_now = date.today()

            conn.begin()
            update_register_by_token(
                token,
                data_json["user"],
                data_json["name"],
                data_json["email"],
                data_json["passwd"],
                date_now,
            )
            rows_affected = cur.rowcount
            conn.commit()

            if rows_affected == 0:
                return return_response(204, "No rows affected")

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

        conn.begin()
        delete_register_by_id(id_user)
        rows_affected = cur.rowcount
        conn.commit()

        if rows_affected == 0:
            return return_response(204, "No rows affected")

        return response
    return response
 