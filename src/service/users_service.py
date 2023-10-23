from flask import jsonify

from connection import cur
from utils import query_to_json
from storage import select_all_users


def get_all_users():
    select_all_users()

    columns = [x[0] for x in cur.description]
    lines = cur.fetchall()

    result = query_to_json(columns, lines)
    result_json = jsonify(result)
    result_json.status_code = 200
    return result_json
 