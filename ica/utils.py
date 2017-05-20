import os
import json
import uuid

from PIL import Image, ImageOps

from ica.models.user import User


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


def get_recommended_users(user, limit=6):
    """
    Algorithm that returns a list of up to six users
    that the current user is recommended to follow
    based on personal profile settings.
    """

    year = user.year
    # major = user.major
    # following = user.following

    users = User.objects(year=year)

    return users[:limit]


def resize_image(upload_folder, filename):
    """
    Creates a 600x600 square thumbnail from an image
    and overwrites it in its current directory
    """

    dimension = (600, 600)
    path = os.path.join(upload_folder, filename)
    img = Image.open(path)
    thumb = ImageOps.fit(img, dimension, Image.ANTIALIAS)
    thumb.save(path)
