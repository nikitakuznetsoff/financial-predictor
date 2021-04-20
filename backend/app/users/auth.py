from flask import Blueprint, request
from flask_httpauth import HTTPBasicAuth

from app.models import User


def login_required():
    def decorator(f):
        if not request.authorization or not request.authorization.password:
            return "missing the authorization header", 401
        token = request.authorization.password
        if not User.verify_auth_token(token):
            return "error with validation access token", 401
        return f
    return decorator
