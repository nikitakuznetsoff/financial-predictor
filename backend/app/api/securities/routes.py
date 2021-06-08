from flask import Blueprint, json, make_response, jsonify, request
from datetime import datetime, timedelta, date
from bson import json_util


from app.repository import securities_repo, users_repo
from app.models import User
from app.controllers import MoexAPI


bp = Blueprint('security', __name__, url_prefix='/api/security')
moex_api = MoexAPI(repo=securities_repo)


@bp.route('', methods=['POST'])
def get_securities():
    try:
        body = request.get_json()
        securities = body.get('ids')
    except:
        return "incorrect request body", 400
    
    result = []
    for s in securities:
        res = securities_repo.get_security_by_id(s)
        del res['_id']
        result.append(res)
    resp = make_response(
        jsonify({'securities': result}), 200
    )
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@bp.route('/<string:security_id>', methods=['GET'])
def get_security_by_id(security_id):
    security = securities_repo.get_security_by_id(security_id)
    if not security:
        return "not found security with this ID", 404

    response_body = json_util.dumps({'security': security})
    resp = make_response(
        response_body, 200
    )
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@bp.route('/<string:security>/description', methods=['GET'])
def get_security_description(security):
    result = moex_api.get_security_description(security)
    resp_body = jsonify({'security': result})
    resp = make_response(resp_body, 200)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@bp.route('/subscriptions', methods=['GET'])
def get_subscriptions():
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
    user = users_repo.get_user_by_id(user_id)
    if not user:
        return "incorrect user id", 400
    
    if not user.subscriptions:
        "user hasn't subscriptions", 204

    general, securities = moex_api.get_subscriptions_history(user.subscriptions)
    result = {
        'general': general,
        'securities': securities
    }
    resp_body = jsonify({'subscriptions': result})
    resp = make_response(resp_body, 200)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp    


@bp.route('/<string:security>/candles', methods=['GET'])
def get_candles(security):
    try:
        start_date = request.args.get('from')
        interval = int(request.args.get('interval'))
    except:
        return "incorrect params", 400
    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return "incorrect start date format", 400
    
    candles = moex_api.get_candles(security, interval, start_date_dt)
    resp_body = jsonify({'candles': candles})
    resp = make_response(resp_body, 200)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp