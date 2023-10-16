import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from os import environ
from dotenv import load_dotenv


load_dotenv()
payload = {
    "username": 'user',
    "exp": datetime.utcnow() + timedelta(hours=1000)
}
secret_key = environ["SECRET_KEY"]
token = jwt.encode(payload, secret_key, algorithm="HS256")


try:
    payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    print(payload)
except ExpiredSignatureError:
    print("Token expirado")
except InvalidTokenError:
    print("Token inválido")
