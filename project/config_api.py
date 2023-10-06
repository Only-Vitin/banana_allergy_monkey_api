from os import environ
from dotenv import load_dotenv

from flask import Flask
from flask_restful import Api


load_dotenv()

app = Flask("Banana Allergy Monkey API")
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = environ["SECRET_KEY"]
api = Api(app)
