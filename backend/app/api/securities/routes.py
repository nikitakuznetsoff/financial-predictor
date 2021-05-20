from flask import Blueprint, make_response, jsonify, request
from datetime import datetime, timedelta, date
from bson import json_util

import requests

from app.repository import securities_repo, users_repo
from app.models import User
from app.api.users import login_required


bp = Blueprint('security', __name__, url_prefix='/api/security')

@bp.route('', methods=['GET'])
def security():
    return "pong", 200


def json_decoder_security_info(arr):
    result = {}
    for v in arr:
        result[v[0]] = {
            'title': v[1],
            'value': v[2]
        }
    return result


@bp.route('/<string:security_id>', methods=['GET'])
def get_security_by_id(security_id):
    securities = securities_repo.get_securities_by_id(security_id)
    if not securities:
        return "not found securities with this ID", 404

    print(securities)
    response_body = json_util.dumps({'securities': securities})
    resp = make_response(
        response_body, 200
    )
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@bp.route('/<string:security>/description', methods=['GET'])
def get_security_description(security):
    url = 'http://iss.moex.com/iss/securities/{0}.json'.format(security)
    r = requests.get(url)
    info = r.json()

    if not info['description']['data']:
        return "empty", 204
    decoded_info = json_decoder_security_info(info['description']['data'])
    resp = make_response(
        jsonify({'security': decoded_info}), 200
    )
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp

###

def get_curr_price_and_name(security_id):
    URL = "http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/57/securities/{0}.json"\
        .format(security_id)
    r = requests.get(URL)
    data = r.json()
    return data['securities']['data'][0][3], data['securities']['data'][0][2]


def get_last_price(security_id, from_date, till_date):
    URL = "http://iss.moex.com/iss/history/engines/stock/" + \
        "markets/shares/sessions/total/boardgroups/57/securities/"+\
        "{0}.json?from={1}&till={2}".format(security_id, from_date, till_date)
    r = requests.get(URL)
    data = r.json()
    last_price = data['history']['data'][-1][11]
    return last_price
    

def get_procent(base, value):
    division = value / base
    if division > 0:
        division = round((division-1) * 100)
    else:
        division = round((1 - division) * 100) * -1
    return division


def get_history_of_security(security_id):    
    today = date.today()
    week = timedelta(days=7)
    month = timedelta(days=31)
    year = timedelta(days=365)
    gap = timedelta(days=3)
    
    curr_price, name = get_curr_price_and_name(security_id)
    week_price = get_last_price(
        security_id, 
        (today-week-gap).strftime("%Y-%m-%d"), 
        (today-week).strftime("%Y-%m-%d")
    )
    month_price = get_last_price(
        security_id, 
        (today-month-gap).strftime("%Y-%m-%d"), 
        (today-month).strftime("%Y-%m-%d")
    )
    year_price = get_last_price(
        security_id, 
        (today-year-gap).strftime("%Y-%m-%d"), 
        (today-year).strftime("%Y-%m-%d")
    )
    result = {
        'id': security_id,
        'name': name,
        'price': curr_price,
        'day': 0,
        'week': get_procent(curr_price, week_price),
        'month': get_procent(curr_price, month_price),
        'year': get_procent(curr_price, year_price),
        'type': 'Акции',
        'currency': 'SUR'
    }
    return result


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

    results = []
    for sub in user.subscriptions:
        results.append(get_history_of_security(sub))
    
    print(results)
    resp_body = jsonify({'subscriptions': results})
    resp = make_response(resp_body, 200)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp    


# Transform data from i: {open, close, high, low, ..} to
# [{x: date, y: {open, hight, low, close}}]
# for ApexCharts
def get_graph_info(candles):
    result = []
    for candle in candles:
        result.append({
            'x': candle[6], # open date
            'y': [candle[0], candle[2], candle[3], candle[1]] # values
        })
    return result

# Transform data from i: {open, close, high, low, value, volume, begin, end} to
# [[timestamp(open), open, high, low, close, volume]]
def get_graph_info_tradingvue(candles):
    indx = {
      'open': 0, 'close': 1, 'high': 2, 'low': 3, 
      'value': 4, 'volume': 5, 'begin': 6, 'end': 7
    }
    result = []
    for i, candle in enumerate(candles):
        dt = datetime.strptime(candle[indx['begin']], "%Y-%m-%d %H:%M:%S")
        timestamp = (dt - datetime(1970, 1, 1)) / timedelta(seconds=1)
        timestamp = int(timestamp) * 1000
        arr = [
          timestamp, candle[indx['open']], 
          candle[indx['high']], candle[indx['low']],
          candle[indx['close']], candle[indx['volume']]
        ]
        result.append(arr)
    return result
    

def get_number_of_candles(start_date: datetime, interval: int):
    "Получение общего количества свечей от указанной стартовой даты и интервала"
    gap = datetime.now() - start_date
    gap_in_minutes = gap.days * 24 * 60
    number_of_candles = int(gap_in_minutes / interval)
    return number_of_candles


def get_interval_in_minutes(interval: int):
    "Получение интервалов из формата москвоской биржи в минуты"
    intervals = [1, 10, 60, 24, 7, 31, 4]
    if interval in intervals[:3]:
        return interval
    if interval == 24:
        return 60 * 24
    if interval == 7:
        return 60 * 24 * 7
    if interval == 31:
        return 60 * 24 * 31
    if interval == 4:
        return 60 * 24 * 31 * 3


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
    
    interval_in_min = get_interval_in_minutes(interval)
    number_of_candles = get_number_of_candles(start_date_dt, interval_in_min)

    # Ссылка для получения инфомрации об акциях
    URL = 'http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/'+\
        '57/securities/{0}/candles.json?from={1}&interval={2}'\
        .format(security, start_date, interval)
    
    candles = []
    r = requests.get(URL)
    if r.status_code != 200:
        return "error with receiving data from moscow exchange", 400
    data = r.json()
    candles.extend(data['candles']['data'])

    # print(repo.get_candles(
    #     security_id=security, interval=interval, start_date=start_date_dt
    # ))

    # Если количество полученных свечей меньше нужного количества, 
    # значит нужно сделать еще некоторое кол-во запросов для получения остальных данных
    max_length_of_candles = len(candles)
    if max_length_of_candles < number_of_candles:
        pointer = max_length_of_candles
        while pointer < number_of_candles:
            URL += "&start={0}".format(pointer)
            r = requests.get(URL)
            if r.status_code != 200:
                return "error with receiving data from moscow exchange", 400
            data = r.json()
            candles.extend(data['candles']['data'])
            pointer += max_length_of_candles

    # graph_info = get_graph_info(candles)
    graph_info_tradingvue = get_graph_info_tradingvue(candles)
    # print(graph_info_tradingvue[0])

    # resp_body = jsonify({'data': graph_info})
    resp_body = jsonify({'candles': graph_info_tradingvue})
    resp = make_response(resp_body, 200)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp
    