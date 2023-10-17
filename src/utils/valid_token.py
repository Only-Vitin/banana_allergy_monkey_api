import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from flask import jsonify
from os import environ
from dotenv import load_dotenv

from utils.response import return_response

load_dotenv()
def valid_token(token):
    secret_key = environ["SECRET_KEY"]
    try:
        jwt.decode(token, secret_key, algorithms=['HS256'])
    except ExpiredSignatureError:
        return return_response(403, "Forbidden")
    except InvalidTokenError:
        return return_response(401, "Unauthorized")
    else:
        return return_response(200, "Ok")
