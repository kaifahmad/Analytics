import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os

def fetch_api_data(url, params=None, headers=None, timeout=10):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

#Plug your parameters here, all are mandatory parameters
from_dt = "2020-01-01"
to_dt = "2025-12-31"
url = "https://kite.zerodha.com"
candle_period = "60minute"
instrument_token = "256265"
user_id = ""

#Plug your parameters here, all are mandatory parameters
header = {
    "authorization" : "",
    "cookie" : ""
}

start_date = datetime.strptime(from_dt, "%Y-%m-%d")
end_date = datetime.strptime(to_dt, "%Y-%m-%d")
current_start = start_date
shard_num = 1

# Create export directory structure
export_dir = os.path.join("export", instrument_token, candle_period)
os.makedirs(export_dir, exist_ok=True)

while current_start <= end_date:
    current_end = current_start + relativedelta(months=3) - relativedelta(days=1)
    if current_end > end_date:
        current_end = end_date

    interval_from = current_start.strftime("%Y-%m-%d")
    interval_to = current_end.strftime("%Y-%m-%d")
    path = f"/oms/instruments/historical/{instrument_token}/{candle_period}"
    params = {
        "user_id": user_id,
        "oi": 1,
        "from": interval_from,
        "to": interval_to
    }

    full_url = url + path

    data = fetch_api_data(full_url, params=params, headers=header)
    if data:
        records = data.get('data', {}).get('candles', [])
        if records:
            df = pd.DataFrame(records)
            csv_filename = f"historical_data_shard_{str(shard_num).zfill(5)}.csv"
            csv_path = os.path.join(export_dir, csv_filename)
            df.to_csv(csv_path, index=False,header=True)
            print(f"Saved {len(df)} records to {csv_path}")
        else:
            print(f"No records found for {interval_from} to {interval_to}")
    else:
        print(f"Failed to fetch data for {interval_from} to {interval_to}")

    current_start = current_end + relativedelta(days=1)
    shard_num += 1
