from flask import Blueprint, request, make_response

from app import repo
from app.models import User

bp = Blueprint('users', __name__, url_prefix='/api/users')


@bp.route('', methods=['POST'])
def create_user():
    data = body.json()
    if 'email' not in data or 'password' not in data:
        return 'incorrect body', 400
    email = data['email']
    password = data['password']
    try:
        user = repo.create_user(
            email=email,
            password=password
        )
    except:
        return 'incorrect data', 400
    return user.id



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
