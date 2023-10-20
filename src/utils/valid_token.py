from os import environ
from dotenv import load_dotenv

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from utils.response import return_response
from storage import search_token
from connection import cur


load_dotenv()
def valid_token(token):
    search_token(token)
    lines = cur.fetchall()
    if len(lines) == 0:
        return return_response(404, "Not Found")
    
    try:
        secret_key = environ["SECRET_KEY"]
        jwt.decode(token, secret_key, algorithms=['HS256'])
    except ExpiredSignatureError:
        return return_response(403, "Forbidden")
    except InvalidTokenError:
        return return_response(401, "Unauthorized")
    else:
        return return_response(200, "Ok")