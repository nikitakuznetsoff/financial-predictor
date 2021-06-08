from flask import Blueprint, request, make_response, jsonify

from app.models import User
from app.repository import users_repo as repo
from datetime import datetime

bp = Blueprint('users', __name__, url_prefix='/api/users')



@bp.route('', methods=['POST', 'GET', 'DELETE'])
def user():
    if request.method == 'POST':
        try:
            body = request.get_json()
            email = body.get('email')
            password = body.get('password')
            username = body.get('username')
        except:
            return "incorrect request body", 400

        user = repo.get_user_by_email(email=email)
        if user:
            return "user exist", 409

        user = repo.get_user_by_username(username=username)
        if user:
            return "user exist", 409
        
        user = repo.create_user(
            email=email, 
            password=password,
            username=username,
            reg_date=datetime.now()
        )
        # try:
        #     user = repo.create_user(
        #         email=email, 
        #         password=password,
        #         username=username,
        #         reg_date=datetime.now()
        #     )
        # except:
        #     return "internal error", 500
        
        user = repo.get_user_by_email(email=email)
        token = user.generate_auth_token().decode('utf-8')
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
            return 'incorrect auth method', 401
        
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

    if request.method == 'DELETE':
        if 'Authorization' not in request.headers:
            return "unauthorized", 401
        try:
            method, token = request.headers['Authorization'].split(' ')
            if method != 'Basic':
                raise Exception
        except:
            return "incorrect auth method or token", 401 
        
        user_id = User.verify_auth_token(token)
        if not user_id:
            return "error with validation access token", 401
        
        user = repo.get_user_by_id(user_id)
        if not user:
            return "incorrect user id", 400
        
        try:
            repo.delete_user(user_id)
        except:
            return "interval error", 500
        return "success", 200
    return "incorrect method", 400


@bp.route('/auth', methods=['POST', 'GET'])
def auth_post():
    if request.method == 'POST':
        body = request.get_json()
        email = body.get('email')
        password = body.get('password')

        user = repo.get_user_by_email(email)
        if not user:
            return "unregistered user", 404
        if not user.verify_password(password):
            return "incorrect password", 400
        
        token = user.generate_auth_token().decode('utf-8')
        d = { 'user': user.id, 'token': token }
        resp = make_response(jsonify(d), 200)
        return resp
    else:
        return "incorrect method", 400


@bp.route('/subscriptions', methods=['GET'])
def get_user_subscriptions():
    if 'Authorization' not in request.headers:
        return "unauthorized", 401
    try:
        method, token = request.headers['Authorization'].split(' ')
    except:
        return "incorrect auth method or token", 401 
    if method != 'Basic':
        return 'incorrect auth method', 401

    user_id = User.verify_auth_token(token)
    if not user_id:
        return "error with validation access token", 401
    user = repo.get_user_by_id(user_id)
    if not user:
        return "incorrect user id", 400

    subs = user.subscriptions
    resp_body = jsonify({'subscriptions': subs})
    resp = make_response(resp_body, 200)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@bp.route('/subscribe', methods=['POST'])
def subscribe():
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
    
    try:
        body = request.get_json()
        secid = body.get('secid')
    except:
        return "incorrect request body", 400
    repo.add_user_subscription(user.id, secid)
    return "subscription successful", 200


@bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
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
    
    body = request.get_json()
    try:
        secid = body.get('secid')
    except:
        return "incorrect request body", 400
    
    try:
        repo.remove_user_subscriptions(user.id, secid)
    except:
        return "server error", 500
    return "unsubscription successful", 200


@bp.route('/username', methods=['POST'])
def change_user_username():
    if 'Authorization' not in request.headers:
        return "unauthorized", 401
    try:
        method, token = request.headers['Authorization'].split(' ')
        if method != 'Basic':
            raise Exception
    except:
        return "incorrect auth method or token", 401 
    
    user_id = User.verify_auth_token(token)
    if not user_id:
        return "error with validation access token", 401
    
    user = repo.get_user_by_id(user_id)
    if not user:
        return "incorrect user id", 400

    try:
        body = request.get_json()
        username = body.get('username')
    except:
        return "incorrect request body", 400

    user = repo.get_user_by_username(username)
    if user:
        return "username already  used", 409

    user = repo.change_username(user_id, username)
    if not user:
        return "interval error", 500
    return "success", 200



@bp.route('/email', methods=['POST'])
def change_user_email():
    if 'Authorization' not in request.headers:
        return "unauthorized", 401
    try:
        method, token = request.headers['Authorization'].split(' ')
        if method != 'Basic':
            raise Exception
    except:
        return "incorrect auth method or token", 401 
    
    user_id = User.verify_auth_token(token)
    if not user_id:
        return "error with validation access token", 401
    
    user = repo.get_user_by_id(user_id)
    if not user:
        return "incorrect user id", 400

    try:
        body = request.get_json()
        email = body.get('email')
    except:
        return "incorrect request body", 400

    user = repo.get_user_by_email(email)
    if user:
        return "email already used", 409
    user = repo.change_email(user_id, email)
    if not user:
        return "interval error", 500
    return "success", 200


@bp.route('/password', methods=['POST'])
def change_user_password():
    if 'Authorization' not in request.headers:
        return "unauthorized", 401
    try:
        method, token = request.headers['Authorization'].split(' ')
        if method != 'Basic':
            raise Exception
    except:
        return "incorrect auth method or token", 401 
    
    user_id = User.verify_auth_token(token)
    if not user_id:
        return "error with validation access token", 401
    
    user = repo.get_user_by_id(user_id)
    if not user:
        return "incorrect user id", 400

    try:
        body = request.get_json()
        password = body.get('password')
    except:
        return "incorrect request body", 400

    user = repo.change_password(user_id, password)
    if not user:
        return "interval error", 500
    return "success", 200


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
