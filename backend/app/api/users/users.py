from flask import Blueprint, request, make_response, jsonify

from app.models import User
from app.repository import users_repo as repo

bp = Blueprint('users', __name__, url_prefix='/api/users')


@bp.route('', methods=['POST', 'GET'])
def get_post_user():
    if request.method == 'POST':
        body = request.get_json()
        email = body.get('email')
        password = body.get('password')

        user = repo.get_user_by_email(email=email)
        if user:
            return "user exist", 400
        
        try:
            user = repo.create_user(email=email, password=password)
        except:
            return "internal error", 500
        
        user = repo.get_user_by_email(email=email)
        token = user.generate_auth_token()
        resp = make_response(jsonify({'user': user.id, 'token': token}), 200)
        return resp
    
    if request.method == 'GET':
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

        user_data = user.get_dict_repr()
        data = { 'user': user_data }
        return make_response(
            jsonify(data),200
        )
    
    return "incorrect method", 400



@bp.route('<int:id>', methods=['GET'])
def get_user(id):
    user = repo.get_user_by_id(id)
    if not user:
        return "incorrect user id", 400
    user_data = user.get_dict_repr()
    resp = make_response(
        jsonify({'data': user_data}), 200
    )
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp
