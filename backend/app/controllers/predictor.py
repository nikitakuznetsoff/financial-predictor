from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing


class Predictor(object):
    def __parameters_selection_arima(self, candles):
        if len(candles) > 500:
            return (1, 1, 1)
        d = range(1, 3)
        q = range(1, 3)

        best_aic = float('inf')
        best_params = ()

        for i in d:
            for j in q:
                try:
                  model = ARIMA(candles, order=(i, 1, j))
                  model_fit = model.fit()
                except:
                  continue
            aic = model_fit.aic
            if aic < best_aic:
                best_aic = aic
                best_params = (i, 1, j)
        return best_params    

    def __parameters_selection_sarima(self, candles):
        if len(candles) > 500:
            return (1, 1, 1)
        d = range(1, 3)
        q = range(1, 3)

        D = range(1, 3)
        Q = range(1, 3)

        best_aic = float('inf')
        best_params = ()

        for i in d:
            for j in q:
                try:
                  model = SARIMAX(candles, order=(i, 1, j))
                  model_fit = model.fit()
                except:
                  continue
            aic = model_fit.aic
            if aic < best_aic:
                best_aic = aic
                best_params = (i, 1, j)
        return best_params

    
    def __get_forecasts(self, candles, prediction_length, params):
        results = []
        data = candles
        for i in range(prediction_length):
            model = ARIMA(data, order=params)
            model_fit = model.fit()
            predict = model_fit.forecast()[0]
            data.append(predict)
            results.append(predict)
        return results


    # def get_arima_predictions(self, candles, prediction_length):
    #     # best_params = self.__parameters_selection_arima(candles)
    #     best_params = (1,1,1)
    #     forecasts = self.__get_forecasts(candles, prediction_length, best_params)
    #     return forecasts

    def get_arima_predictions(self, candles, prediction_length):
        model = ARIMA(candles, order=(2,2,1))
        model_fit = model.fit()
        result = model_fit.forecast(steps=prediction_length)
        return result.tolist()


    def get_sarima_predictions(self, candles, prediction_length):
        # best_params = self.__parameters_selection_sarima(candles)
        model = SARIMAX(candles, order=(1,1,1), seasonal_order=(1,1,1,12))
        model_fit = model.fit()
        result = model_fit.forecast(steps=prediction_length)
        return result.tolist()


    def get_smooth_predictions(self, candles, prediction_length):
        results = []
        data = candles
        for i in range(prediction_length):
            model = ExponentialSmoothing(data, trend="add", initialization_method="estimated")
            model_fit = model.fit()
            predict = model_fit.predict()[0]
            results.append(predict)
            data.append(predict)
        return results
