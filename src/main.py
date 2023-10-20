from os import environ
from dotenv import load_dotenv

from flask import Flask
from flask_restful import Api

from controller import User, Login, Users, VerifyUserEmail

load_dotenv()

app = Flask("Banana Allergy Monkey API")
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = environ["SECRET_KEY"]
api = Api(app)

api.add_resource(User, "/user")
api.add_resource(Users, "/users")
api.add_resource(Login, "/login")
api.add_resource(VerifyUserEmail, "/verify/<string:info>")

if __name__ == "__main__":
    app.run()
