import json
import uuid


def get_file_extension(filename):
    """
    Extracts file extension from a file name
    Ex: png from pfpic.png
    """
    return filename.rsplit('.', 1)[1].lower()


def allowed_filename(filename, whitelist):
    """Determines if the file extension is in the whitelist"""
    return '.' in filename and \
           get_file_extension(filename) in whitelist


def generate_token():
    """Generates unique profile picture token"""
    return uuid.uuid4().hex


def jsonify_response(resp):
    """
    Converts a Flask Response object to a deserialized
    JSON instance to Python object
    """
    resp_string = resp.get_data().decode('utf-8')
    return json.loads(resp_string)
