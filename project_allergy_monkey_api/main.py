from flask import Flask
from flask_restful import Api

from routes import Register, VerificaLogin


app = Flask("Banana Allergy Monkey API")
app.config["JSON_SORT_KEYS"] = False
api = Api(app)

api.add_resource(Register, "/register")
api.add_resource(VerificaLogin, "/check_login")


if __name__ == "__main__":
    app.run()
