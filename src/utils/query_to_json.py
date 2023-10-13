import json
from datetime import date


def query_to_json(columns, lines):
    data_list = []
    for result in lines:
        result = [str(value) if isinstance(value, date) else value for value in result]
        data_list.append(dict(zip(columns, result)))
    result_json = json.dumps(data_list)
    result_json = json.loads(result_json)
    return result_json
