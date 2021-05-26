from flask import Blueprint, make_response, jsonify, request
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime
import json

from app.repository import users_repo as repo
from app.controllers import Predictor

bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')
predictor = Predictor()


@bp.route('', methods=['POST'])
def tasks():
    try:
        body = request.get_json()
        candles = body.get('candles')
        algo = body.get('algo')
        predictions_number = body.get('count')
    except:
        "incorrect request body", 400

    cndls = [x[1] for x in candles]
    prediction = []
    if algo == "ARIMA":
        prediction = predictor.get_arima_predictions(
            candles=cndls,
            prediction_length=predictions_number   
        )
    elif algo == "SARIMA":
        prediction = predictor.get_sarima_predictions(
            candles=cndls,
            prediction_length=predictions_number   
        )
    elif algo == "HWES":
        prediction = predictor.get_smooth_predictions(
            candles=cndls,
            prediction_length=predictions_number   
        )
    else:
        return "incorrect algo name", 400
    print(candles)
    print('***')
    print(prediction)
    body_d = {
        'prediction': {
            'values': prediction
        }
    }
    resp_body = jsonify(body_d)
    return make_response(resp_body, 200)
