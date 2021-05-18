from flask import Blueprint, make_response, jsonify, request
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime

from app.repository import users_repo as repo

bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@bp.route('', methods=['GET'])
def tasks():
    return 'pong', 200


@bp.route('/<int:id>', methods=['GET'])
def get_task_status(id):
    task = repo.get_task_status(id)
    if not id:
        return "incorrect id", 400
    else:
        return task.is_completed, 200


@bp.route('/ma', methods=['GET', 'POST'])
def get_ma_prediction():
    try:
        body = request.get_json()
        candles = body.get('data')
    except:
        return "incorrect request body", 400

    model = ARIMA([x['y'][0] for x in candles], order=(0,0,1))
    model_fit = model.fit()
    y_hat = model_fit.predict(len(candles), len(candles))


    dt_0 = datetime.strptime(candles[0]['x'], "%Y-%m-%d %H:%M:%S")
    dt_1 = datetime.strptime(candles[1]['x'], "%Y-%m-%d %H:%M:%S")
    gap = dt_1 - dt_0
    # print(gap)
    gap_in_min = gap.total_seconds() / 60

    last_date = datetime.strptime(candles[-1]['x'], "%Y-%m-%d %H:%M:%S")
    # print(last_date)
    predict_date = last_date + gap
    str_date = predict_date.strftime("%Y-%m-%d %H:%M:%S")
    # print(str_date)

    resp_body = {'prediction': y_hat[0], 'interval': gap_in_min, 'date': str_date}
    return make_response(jsonify(resp_body), 200)


@bp.route('/arma', methods=['GET', 'POST'])
def get_arma_prediction():
    try:
        body = request.get_json()
        candles = body.get('data')
    except:
        return "incorrect request body", 400

    model = ARIMA([x['y'][0] for x in candles], order=(2,0,1))
    model_fit = model.fit()
    y_hat = model_fit.predict(len(candles), len(candles))

    dt_0 = datetime.strptime(candles[0]['x'], "%Y-%m-%d %H:%M:%S")
    dt_1 = datetime.strptime(candles[1]['x'], "%Y-%m-%d %H:%M:%S")
    gap = dt_1 - dt_0
    # print(gap)
    gap_in_min = gap.total_seconds() / 60

    last_date = datetime.strptime(candles[-1]['x'], "%Y-%m-%d %H:%M:%S")
    # print(last_date)
    predict_date = last_date + gap
    str_date = predict_date.strftime("%Y-%m-%d %H:%M:%S")
    # print(str_date)

    resp_body = {'prediction': y_hat[0], 'interval': gap_in_min, 'date': str_date}
    return make_response(jsonify(resp_body), 200)


@bp.route('/arima', methods=['GET', 'POST'])
def get_arima_prediction():
    try:
        body = request.get_json()
        candles = body.get('data')
    except:
        return "incorrect request body", 400

    model = ARIMA([x['y'][0] for x in candles], order=(1,1,1))
    model_fit = model.fit()
    y_hat = model_fit.predict(len(candles), len(candles), typ='levels')
   
    dt_0 = datetime.strptime(candles[0]['x'], "%Y-%m-%d %H:%M:%S")
    dt_1 = datetime.strptime(candles[1]['x'], "%Y-%m-%d %H:%M:%S")
    gap = dt_1 - dt_0
    # print(gap)
    gap_in_min = gap.total_seconds() / 60

    last_date = datetime.strptime(candles[-1]['x'], "%Y-%m-%d %H:%M:%S")
    # print(last_date)
    predict_date = last_date + gap
    str_date = predict_date.strftime("%Y-%m-%d %H:%M:%S")
    # print(str_date)

    resp_body = {'prediction': y_hat[0], 'interval': gap_in_min, 'date': str_date}
    return make_response(jsonify(resp_body), 200)


@bp.route('/sarima', methods=['GET', 'POST'])
def get_sarima_prediction():
    try:
        body = request.get_json()
        candles = body.get('data')
    except:
        return "incorrect request body", 400

    model = SARIMAX([x['y'][0] for x in candles], order=(1,1,1), seasonal_order=(0,0,0,0))
    model_fit = model.fit(disp=False)
    y_hat = model_fit.predict(len(candles), len(candles))
    
    dt_0 = datetime.strptime(candles[0]['x'], "%Y-%m-%d %H:%M:%S")
    dt_1 = datetime.strptime(candles[1]['x'], "%Y-%m-%d %H:%M:%S")
    gap = dt_1 - dt_0
    # print(gap)
    gap_in_min = gap.total_seconds() / 60

    last_date = datetime.strptime(candles[-1]['x'], "%Y-%m-%d %H:%M:%S")
    # print(last_date)
    predict_date = last_date + gap
    str_date = predict_date.strftime("%Y-%m-%d %H:%M:%S")
    # print(str_date)

    resp_body = {'prediction': y_hat[0], 'interval': gap_in_min, 'date': str_date}
    return make_response(jsonify(resp_body), 200) 



