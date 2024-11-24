from flask import jsonify


class HttpError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


def error_handler(error: HttpError):
    http_response = jsonify({"error": error.message})
    http_response.status_code = error.status_code
    return http_response