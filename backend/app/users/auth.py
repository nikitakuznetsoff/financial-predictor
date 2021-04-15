from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/get', methods=['GET'])
def auth_get():
    pass

@bp.route('/get_code', methods=['GET'])
def auth_get_code():
    pass

