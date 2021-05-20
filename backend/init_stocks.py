import requests
from app.repository import mongo_client as client

URL = 'http://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/'+\
        '57/securities.json'

r = requests.get(URL)
data = r.json()

for stock in data['securities']['data']:
    d = {
      'secid': stock[0],
      'name': stock[2],
      'type': 'Акции'
    }
    client.finPredictor.securities.insert_one(d)