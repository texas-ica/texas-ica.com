import json


def jsonify_response(resp):
    """
    Converts a Flask Response object to a deserialized
    JSON instance to Python object
    """
    resp_string = resp.get_data().decode('utf-8')
    return json.loads(resp_string)
