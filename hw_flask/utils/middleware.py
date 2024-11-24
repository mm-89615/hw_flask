import flask
from flask import request

from hw_flask.utils.db import Session


def before_request():
    session = Session()
    request.session = session


def after_request(response: flask.Response):
    request.session.close()
    return response