class APIError(Exception):
    status_code = 400

    def __init__(self, message):
        super(APIError, self).__init__()
        self.message = message

    def to_dict(self):
        return {'error': self.message}


class APIBadRequestError(APIError):
    status_code = 400


class APIForbiddenError(APIError):
    status_code = 403


class APINotFoundError(APIError):
    status_code = 404
