"""
@Author: Kaif Ahmad
@Email: kaifahmad111@gmail.com
@Python Version: Python 3.11.4
@pip version: pip 23.1.2
"""
import json
import os
from datetime import datetime,timedelta
import subprocess
from util import write_to_csv, fetch_data

LOAD_INTERVAL = 1

with open('./config/param_config.json','r') as f:
  url_config = json.load(f)

i_date = url_config['from_date']
to_date = url_config['to_date']
if not os.path.exists('./output'):
    os.mkdir('./output')

# remove old file
os.remove("./output/nifty.csv") if os.path.exists("./output/nifty.csv") else None    

while (datetime.strptime(i_date,'%Y-%m-%d') <= datetime.strptime(to_date,'%Y-%m-%d')):
    
    start = i_date
    # try:
    #   line = subprocess.check_output(['tail', '-1', "./output/nifty.csv"]).decode('utf-8').strip('\r\n')
    #   candle = line.split(',')[-1]
    #   close = line.split(',')[4]
    # except Exception:
    close = 0
    end_obj = datetime.strptime(i_date,'%Y-%m-%d') + timedelta(days=LOAD_INTERVAL)
    end = end_obj.strftime('%Y-%m-%d')
    response_dict = fetch_data(start, end)
    write_to_csv(p_candles = response_dict["data"]["candles"], ) 
    i_date = (end_obj + timedelta(days = 1)).strftime('%Y-%m-%d')

        