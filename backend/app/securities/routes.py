from flask import Blueprint, make_response, jsonify
from datetime import datetime
import requests

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


@bp.route('/<string:security>', methods=['GET'])
def get_security_info(security):
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

# Transform data from i: {open, close, high, low, ..} to
# [{x: date, y: {open, hight, low, close}}]
def get_graph_info(candles):
    result = []
    for candle in candles['candles']['data']:
        result.append({
            'x': candle[6], # open date
            'y': [candle[0], candle[2], candle[3], candle[1]] # values
        })
    return result

    
@bp.route('/<string:security>/<string:start_date>/<int:interval>', methods=['GET'])
def get_candles(security, start_date, interval):
    try:
        dt = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return "incorrect start date", 400

    # Для акций
    url = 'http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/'+\
        '57/securities/{0}/candles.json?from={1}&interval={2}'.format(security, start_date, interval)
    r = requests.get(url)
    if r.status_code != 200:
        return "error", 400
    candles = r.json()
    graph_info = get_graph_info(candles)
    resp = make_response(
        jsonify({'data': graph_info}), 200
    )
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp
    
