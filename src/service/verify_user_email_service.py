from utils import return_response, verify_none_values_json
from storage import search_user, search_email
from connection import cur


def verify_info_on_db(info, data_json):
    null_on_data = verify_none_values_json(data_json)
    if null_on_data is False:
        try:
            if info == "user":
                user = data_json["user"]
                search_user(user)
            elif info == "email":
                email = data_json["email"]
                search_email(email)
            else:
                return return_response(404, "Not Found")
        except KeyError:
            return return_response(400, "Bad Request")

        lines = cur.fetchall()
        if len(lines) == 0:
            return return_response(200, "Not in database")
        return return_response(409, "Already registered")
    return null_on_data
