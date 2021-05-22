from flask import Blueprint, request, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from functools import wraps

from app.models import User
from app.repository import users_repo as repo

 
def login_required(func):
    @wraps(func)
    def decorator(f):
        if 'Authorization' not in request.headers:
            return "unauthorized", 401
        try:
            method, token = request.headers['Authorization'].split(' ')
        except:
            return "incorrect auth method or token", 401 
        
        if method != 'Basic':
            'incorrect auth method', 401
        
        user_id = User.verify_auth_token(token)
        if not user_id:
            return "error with validation access token", 401
        
        user = repo.get_user_by_id(user_id)
        if not user:
            return "incorrect user id", 400
        return f
    if func:
        return decorator(func)
    return decorator

