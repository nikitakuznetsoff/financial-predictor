from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth = HTTPBasicAuth()


def login_required():
    def decorator(f):
        
        return f
    return decorator




@bp.route('/get', methods=['GET'])
@auth.login_required
def auth_get():
    pass

@bp.route('/get_code', methods=['GET'])
def auth_get_code():
    pass

