import requests
from datetime import date, timedelta, datetime


class MoexAPI:
    def __init__(self, repo):
        self.base_url = 'http://iss.moex.com/iss/'
        self.repo = repo


    def __json_decoder_security_info(arr):
        result = {}
        for v in arr:
            result[v[0]] = {
                'title': v[1],
                'value': v[2]
            }
        return result
        

    def get_security_description(self, security_id):
        url = self.base_url + 'securities/{0}.json'.format(security_id)
        r = requests.get(url)
        info = r.json()

        if not info['description']['data']:
            return "empty", 204

        decoded_info = self.__json_decoder_security_info(info['description']['data'])
        return decoded_info

    def get_current_price(self, security_id):
        "Получить текущую цену инструмента, цену на момент начала торгов в этот день"
        URL = "http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/57/securities/{0}.json"\
            .format(security_id)
        r = requests.get(URL)
        data = r.json()
        return data['marketdata']['data'][0][9], data['marketdata']['data'][0][12]




    def __get_last_price(self, security_id, from_date, till_date):
        "Получить цену инструмента по закрытию торгов в указанный период (период для случая, когда заданная дата - выходной)"
        URL = "http://iss.moex.com/iss/history/engines/stock/" + \
            "markets/shares/sessions/total/boardgroups/57/securities/"+\
            "{0}.json?from={1}&till={2}".format(security_id, from_date, till_date)
        r = requests.get(URL)
        data = r.json()
        if not data['history']['data']:
            return None
        last_price = data['history']['data'][-1][11]
        return last_price
        

    def __get_procent(self, base, value):
        "Получить изменение стоимости инструмента в процентном выражении"
        if not value:
            return 0
        division = value / base
        if division > 0:
            division = round((division-1) * 10000) / 100
        else:
            division = round((1 - division) * 10000) / 100 * -1
        return division


    def __get_history_of_security(self, security_id):
        "Получить историю стоимости заданного финансового инструмента"    
        today = date.today()
        week = timedelta(days=7)
        month = timedelta(days=31)
        year = timedelta(days=365)
        gap = timedelta(days=3)
        
        security = self.repo.get_securities_by_id(security_id)[0]
        curr_price, start_price = self.__get_current_price(security_id)
        week_price = self.__get_last_price(
            security_id, 
            (today-week-gap).strftime("%Y-%m-%d"), 
            (today-week).strftime("%Y-%m-%d")
        )
        month_price = self.__get_last_price(
            security_id, 
            (today-month-gap).strftime("%Y-%m-%d"), 
            (today-month).strftime("%Y-%m-%d")
        )
        year_price = self.__get_last_price(
            security_id, 
            (today-year-gap).strftime("%Y-%m-%d"), 
            (today-year).strftime("%Y-%m-%d")
        )
        result = {
            'id': security_id,
            'name': security['name'],
            'price': curr_price,
            'day': self.__get_procent(curr_price, start_price),
            'week': self.__get_procent(curr_price, week_price),
            'month': self.__get_procent(curr_price, month_price),
            'year': self.__get_procent(curr_price, year_price),
            'type': 'Акции',
            'currency': 'SUR'
        }
        return result

    
    def __get_general_history(self, securities):
        "Получить историю общей стоимости финансовых инструментов из списка"
        res = {
            'day': 0,
            'week': 0,
            'month': 0,
            'year': 0
        }
        for sec in securities:
            res['day'] += sec['day']
            res['week'] += sec['week']
            res['month'] += sec['month']
            res['year'] += sec['year']

        N = len(securities)
        res['day'] = round(res['day'] / N * 100) / 100
        res['week'] = round(res['week'] / N * 100) / 100
        res['month'] = round(res['month'] / N * 100) / 100
        res['year'] = round(res['year'] / N * 100) / 100
        return res


    def get_subscriptions_history(self, subscriptions):
        results = []
        for sub in subscriptions:
            results.append(self.__get_history_of_security(sub))
        general = self.__get_general_history(results)
        return general, results


    def __get_interval_in_minutes(self, interval: int):
        "Преобразование интервалов свечей из формата москвоской биржи в минуты"
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

    def __get_number_of_candles(self, start_date: datetime, interval: int):
        "Получение общего количества свечей от указанной стартовой даты и интервала"
        gap = datetime.now() - start_date
        gap_in_minutes = gap.days * 24 * 60
        number_of_candles = int(gap_in_minutes / interval)
        return number_of_candles

    # Transform data from i: {open, close, high, low, value, volume, begin, end} to
    # [[timestamp(open), open, high, low, close, volume]]
    def __get_graph_info_tradingvue(self, candles):
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


    def get_candles(self, security, interval, start_date_dt):
        interval_in_min = self.__get_interval_in_minutes(interval)
        number_of_candles = self.__get_number_of_candles(start_date_dt, interval_in_min)

        # Ссылка для получения инфомрации об акциях
        URL = 'http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/'+\
            '57/securities/{0}/candles.json?from={1}&interval={2}'\
            .format(security, start_date_dt.strftime("%Y-%m-%d"), interval)
        
        candles = []
        r = requests.get(URL)
        if r.status_code != 200:
            return "error with receiving data from moscow exchange", 400
        data = r.json()
        candles.extend(data['candles']['data'])

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
        transformed_candles = self.__get_graph_info_tradingvue(candles)
        return transformed_candles
      