import asyncio
import aiohttp
import json
import datetime
import requests


class MongoRepository:
    def __init__(self):
        self.client = None
    

    def set_client(self, client):
        self.client = client


    async def _insert_description(self, data):
        result = await self.client.securities.insert_one(data)
        return result


    async def _get_description_from_mongo(self, security_id):
        description = await self.client.securities.find_one({
            'index': security_id
        })
        return description

    # from [v0, v1, v2] to v0: {title: v1, value: v2}
    def _change_security_description_format(self, data):
        result = {}
        for v in data:
            result[v[0]] = {
                'title': v[1],
                'value': v[2]
            }
        return result


    async def _get_description_from_moex(self, security_id):
         async with aiohttp.ClientSession() as session:
            url = 'http://iss.moex.com/iss/securities/{0}.json'.format(security_id)
            async with session.get(url) as response:
                data = response.text()
                return data
    

    # Получение информации о финансовом инструменте
    def get_security_info(self, security_id):
        loop = asyncio.get_event_loop()
        description = loop.run_until_complete(self._get_description(security_id))

        # Если описания нет в монге, то идем на биржу
        if not description:
            data = loop.run_until_complete(self._get_description_from_moex(security_id))
            if not data:
                return None

            data_decoded = json.loads(data)
            data_changed = self._change_security_description_format(data_decoded)
            
            result = loop.run_until_complete(self._insert_description(data_changed))
            if not result:
                return None

            description = data_changed
        return description
    
    def _get_number_of_required_candles(self, interval, start_date):
            gap = datetime.datetime.now() - start_date
            gap_in_minutes = gap.days * 24 * 60
            number_of_candles = int(gap_in_minutes / interval)
            return number_of_candles


    async def _get_candles_from_mongo(self, security_id, interval, start_date):
        candles = await self.client.candles.find({
            'index': security_id,
            'interval': interval,
            'start_date': { '$gte': { start_date } }
        })
        return candles


    async def _get_candles_from_moex(self, security_id, interval, start_date):
        async with aiohttp.ClientSession() as session:
            url = 'http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/'+\
                '57/securities/{0}/candles.json?from={1}&interval={2}'\
                .format(security_id, start_date, interval)
            async with session.get(url) as response:
                data = response.text()
                return json.loads(data)


    # Получение свечей по заданным параметрам
    # def get_candles(self, security_id, interval, start_date):
    #     loop = asyncio.get_event_loop()
    #     asyncio.set_event_loop(loop)
    #     total_number_of_candles = self._get_number_of_required_candles(interval, start_date)

    #     candles = loop.run_until_complete(
    #         self._get_candles_from_mongo(security_id, interval, start_date)
    #     )
    #     if len(candles) < total_number_of_candles:
    #         # Получить инфу от moex
    #         candles = self._get_candles_from_moex(security_id, interval, start_date)
    #     return candles    
    def get_candles(self, security_id, interval, start_date):
        total_number_of_candles = self._get_number_of_required_candles(interval, start_date)
        candles = self.client.finpred.candles.find({
            "index": security_id,
            "interval": interval,
            "start_date": { "$gte": { start_date } }
        })
        if candles.count() < total_number_of_candles:
            URL = 'http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/'+\
                '57/securities/{0}/candles.json?from={1}&interval={2}'\
                .format(security_id, start_date, interval)
            r = requests.get(URL)
            if r.status_code != 200:
                return "error with receiving data from moscow exchange", 400
            candles = r.json()
        return candles  


    
