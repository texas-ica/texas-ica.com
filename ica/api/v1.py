from flask import Blueprint, jsonify

from ica.models.user import User

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def get_users():
    """
    Gets all members of the ICA social network

    URL: /api/v1/users/
    Method: GET
    URL params: None
    """
    users = [user.to_dict() for user in User.objects]
    return jsonify({
        'success': True,
        'users': users
    })


@api.route('/users/<string:query>', methods=['GET'])
def get_users_by_search(query):
    """
    Searches members (first name and last name) through
    query string and returns relevant results

    URL: /api/v1/users/<query>
    METHOD: GET
    URL params: None
    """
    users = User.objects.search_text(query)

    if users:
        users = [user.to_dict() for user in users]
    else:
        users = None

    return jsonify({
        'success': True,
        'users': users
    })


@api.route('/user/<string:email>', methods=['GET'])
def get_user_by_email(email):
    """
    Retrieves a specific user by his/her email

    URL: /api/v1/user/<email>
    METHOD: GET
    URL params: None
    """
    user = User.objects(email=email).first()

    if user:
        user = user.to_dict()

    return jsonify({
        'success': True,
        'user': user
    })
