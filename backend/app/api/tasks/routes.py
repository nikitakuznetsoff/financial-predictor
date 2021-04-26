from flask import Blueprint, make_response, jsonify, request
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

from app.repository import repo

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

    resp_body = {'prediction': y_hat[0]}
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

    resp_body = {'prediction': y_hat[0]}
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
    resp_body = {'prediction':  y_hat[0]}
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
    resp_body = {'prediction': y_hat[0]}
    return make_response(jsonify(resp_body), 200) 



