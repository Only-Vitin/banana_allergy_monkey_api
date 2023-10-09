import json
import bcrypt

from datetime import date

from flask_restful import Resource
from flask import jsonify, request, make_response

from connection import cur


def query_to_json(columns, lines):
    data_list = []
    for result in lines:
        result = [str(value) if isinstance(value, date) else value for value in result]
        data_list.append(dict(zip(columns, result)))
    result_json = json.dumps(data_list)
    result_json = json.loads(result_json)
    return result_json


class User(Resource):

    def get(self):
        token = request.headers.get('Authorization')
        if token:
            cur.execute(f'''SELECT a.*, b.* FROM user a INNER JOIN token b ON a.id = b.id WHERE b.token = "{token}"''')
        else:
            cur.execute("SELECT * FROM token;")

        columns = [x[0] for x in cur.description]
        lines = cur.fetchall()

        result = query_to_json(columns, lines)
        result_json = jsonify(result)
        result_json.status_code = 200
        return make_response(result_json)

    def post(self):
        data_json = request.json

        passwd = data_json["passwd"]
        passwd = passwd.encode('utf-8')
        
        hash = bcrypt.hashpw(passwd, bcrypt.gensalt())
        data_json["passwd"] = hash

        date_now = date.today()
        cur.execute(f'''INSERT INTO user (user, email, name, passwd, registration_date) 
            VALUES("{data_json['user']}", "{data_json['email']}", "{data_json['name']}", "{data_json['passwd']}", "{date_now}");''')
        
        response = jsonify({"message" : "Created"})
        response.status_code = 201
        return make_response(response)

    def put(self, id):
        ...

    def patch(self, id):
        ...

    def delete(self, id):
        ...
