from flask import Blueprint

bp = Blueprint('users', __name__, url_prefix='/api/users')


@bp.route('', methods=['POST'])
def create_user():
    pass