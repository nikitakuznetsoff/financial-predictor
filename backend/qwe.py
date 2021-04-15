import requests
import json

url = 'http://iss.moex.com/iss/securities/{0}.json'.format('AAPLL')
r = requests.get(url)
v = r.json()
print(v)