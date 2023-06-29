"""
@Author: Kaif Ahmad
@Email: kaifahmad111@gmail.com
@Python Version: Python 3.11.4
@pip version: pip 23.1.2
"""
import json
import os
import requests
# from datetime import date,time,timedelta,timezone
from datetime import datetime

headers = {'authorization': 'enctoken Lq0JF4X55rHl8mKpcVR1N5lwCwZnmAtoV1/VNJntGyvYFqenLcg74dXTax5zEopb4OfHmaEHiV7SlA80BtZNY0XLEUUUojCvlGIJ4XN8kcfRmPyqtzkZlg=='}
x = requests.get(
    # url = 'https://kite.zerodha.com/oms/instruments/historical/256265/15minute?user_id=QV8945&oi=1&from=2022-01-01&to=2022-06-01',
    url = 'https://kite.zerodha.com/oms/instruments/historical/256265/15minute?user_id=QV8945&oi=1&from=2022-01-01&to=2022-06-01',
    headers=headers
    )
respose = json.loads(x.text)
# print(respose["data"]["candles"])
print (len(respose["data"]["candles"]))
dt_string = "2023-06-29T15:00:00+0530"
dt_object1 = datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S%z")
# print("dt_object1 =", dt_object1)
# print("dt_object1 =", dt_object1.year, dt_object1.weekday())

if not os.path.exists('./output'):
    os.mkdir('./output')

for candle in respose["data"]["candles"]:
    f = open("./output/nifty.csv", "a")
    f.write(",".join(str(c) for c in candle))
    f.write("\n")
    f.close()
        