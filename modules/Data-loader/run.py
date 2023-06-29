"""
@Author: Kaif Ahmad
@Email: kaifahmad111@gmail.com
@Python Version: Python 3.11.4
@pip version: pip 23.1.2
"""
import json
import os
import requests
from datetime import datetime,timedelta
from util import write_to_csv, fetch_data


with open('./config/param_config.json','r') as f:
  url_config = json.load(f)

i_date = url_config['from_date']
to_date = url_config['to_date']
while (datetime.strptime(i_date,'%Y-%m-%d') <= datetime.strptime(to_date,'%Y-%m-%d')):
   start = i_date
   end_obj = datetime.strptime(i_date,'%Y-%m-%d') + timedelta(days=60)
   end = end_obj.strftime('%Y-%m-%d')
   print(start,end)
   response_dict = fetch_data(start, end)
   write_to_csv(candles=response_dict["data"]["candles"]) 
   i_date = (end_obj + timedelta(days = 1)).strftime('%Y-%m-%d')
    
   
# print(respose["data"]["candles"])
# print (len(respose["data"]["candles"]))
# dt_string = "2023-06-29T15:00:00+0530"
# dt_object1 = datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S%z")
# print("dt_object1 =", dt_object1)
# print("dt_object1 =", dt_object1.year, dt_object1.weekday())
#    "status": "error",
# "status": "success",

if not os.path.exists('./output'):
    os.mkdir('./output')


        