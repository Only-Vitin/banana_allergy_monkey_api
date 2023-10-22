from utils.response import return_response


def verify_none_values_json(data_json):
    for _, value in data_json.items():
        value = value.replace(" ", "")
        if value is None or value == "":
            return return_response(400, "Contains null values")
    return False
