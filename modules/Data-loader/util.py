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


def write_to_csv(candles:list):
    """
    Writes data to the csv file
    """
    for candle in candles:
        f = open("./output/nifty.csv", "a")
        f.write(",".join(str(c) for c in candle))
        f.write("\n")
        f.close()