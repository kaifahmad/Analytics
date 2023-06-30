from datetime import datetime
import json
import requests

def fetch_data(start, end)-> dict:
    """
    Fetches data from the API
    """ 
    BASE_URL = "https://kite.zerodha.com/oms/instruments/historical"
    with open('./config/param_config.json','r') as f:
        url_config = json.load(f)
    headers = {'authorization': url_config["token"]}
    print(f"{BASE_URL}/{url_config['zerodha_code']}/{url_config['time_frame']}?user_id={url_config['user_id']}&oi=1&from={start}&to={end}")
    x = requests.get(
        url = f"{BASE_URL}/{url_config['zerodha_code']}/{url_config['time_frame']}?user_id={url_config['user_id']}&oi=1&from={start}&to={end}",
        headers=headers
        )
    return json.loads(x.text)


def write_to_csv(p_candles:list, p_prevClose):
    """
    Writes data to the csv file
    """
    i_date = p_candles[0][0].split('T')[0]
    close = p_candles[0][4]
    for candle in p_candles:
        candle.pop()

        dt_object1 = datetime.strptime(candle[0], "%Y-%m-%dT%H:%M:%S%z")
        if not i_date == dt_object1.date():
            p_prevClose = close
            i_date = dt_object1.date()

        candle.append(dt_object1.date())
        candle.append(dt_object1.weekday())
        candle.append(f"T{dt_object1.hour}_{dt_object1.minute}")
        candle.append(f"{round(candle[4] - p_prevClose , 2)}")
        candle.append(f"{round(((candle[4] - p_prevClose)/p_prevClose)*100 , 2)}")
        print(candle[0],candle[4],p_prevClose)
        
        close = candle[4]

        f = open("./output/nifty.csv", "a")
        f.write(",".join(str(c) for c in candle))
        f.write("\n")
        f.close()