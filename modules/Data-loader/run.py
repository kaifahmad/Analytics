"""
@Author: Kaif Ahmad
@Email: kaifahmad111@gmail.com
@Python Version: Python 3.11.4
@pip version: pip 23.1.2
"""
import json
import os
from datetime import datetime, timedelta
import subprocess
import tracemalloc
from util import write_to_csv, fetch_data

LOAD_INTERVAL = 300

tracemalloc.start()

with open("./config/param_config.json", "r") as f:
    url_config = json.load(f)

i_date = url_config["from_date"]
to_date = url_config["to_date"]
if not os.path.exists("./output"):
    os.mkdir("./output")

# remove old file
os.remove(f"./output/niftybank_{url_config['time_frame']}.csv") if os.path.exists(
    f'./output/niftybank_{url_config["time_frame"]}.csv'
) else None

while datetime.strptime(i_date, "%Y-%m-%d") <= datetime.strptime(to_date, "%Y-%m-%d"):
    start = i_date
    try:
        line = (
            subprocess.check_output(["tail", "-1", f"./output/niftybank_{url_config['time_frame']}.csv"])
            .decode("utf-8")
            .strip("\r\n")
        )
        close = float(line.split(",")[4])
    except Exception:
        close = 0
    end_obj = datetime.strptime(i_date, "%Y-%m-%d") + timedelta(days=LOAD_INTERVAL)
    end = end_obj.strftime("%Y-%m-%d")
    response_dict = fetch_data(start, end)
    # print(response_dict)
    if len(response_dict["data"]["candles"]) > 0:
        write_to_csv(
            p_candles=response_dict["data"]["candles"],
            p_prevClose=close,
            p_frame=url_config["time_frame"],
        )
    i_date = (end_obj + timedelta(days=1)).strftime("%Y-%m-%d")

print(tracemalloc.get_traced_memory())
tracemalloc.stop()
