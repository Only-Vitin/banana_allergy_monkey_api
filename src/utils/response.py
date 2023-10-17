from flask import jsonify


def return_response(code, message):
    response = jsonify({"message" : f"{message}"})
    response.status_code = code
    return response
