import requests
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA


def get_graph_info(candles):
    result = []
    for candle in candles['candles']['data']:
        result.append({
            'x': candle[6], # open date
            'y': [candle[0], candle[2], candle[3], candle[1]] # values
        })
    return result


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
    return graph_info


candels = get_candles("AFLT", "2021-04-16", 10)
arima = ARIMA([x['y'][0] for x in candels], order=(1,1,1))
model_fit = arima.fit()

yhat = model_fit.predict(len(candels), len(candels), typ='levels')
print(yhat)