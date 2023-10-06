from config_api import app, api
from routes import Register, VerificaLogin

api.add_resource(Register, "/register")
api.add_resource(VerificaLogin, "/check_login")

if __name__ == "__main__":
    app.run()
