from flask import Blueprint, request, make_response, jsonify
from flask_httpauth import HTTPBasicAuth

from app.models import User
from app.repository import users_repo as repo


bp = Blueprint('login', __name__, url_prefix='/api/login')

def login_required():
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
    return decorator


@bp.route('', methods=['POST', 'GET'])
def auth_post():
    if request.method == 'POST':
        body = request.get_json()
        email = body.get('email')
        password = body.get('password')

        user = repo.get_user_by_email(email)
        if not user:
            return "unknown user", 404
        if not user.verify_password(password):
            return "incorrect password", 400
        
        token = user.generate_auth_token()
        d = { 'user': user.id, 'token': token }
        resp = make_response(jsonify(d), 200)
        return resp
    else:
        return "incorrect method", 400
