from datetime import datetime
import json


def write_to_csv(p_timestamp:str, p_exit_candle: list, p_entry_price, p_captured_points, p_direction,p_candle):
    """
    Writes the outcome to the csv file
    """
    
    out_rec = []
    months = json.load(open('./config/const-config.json'))["months"]
    direction = json.load(open('./config/const-config.json'))["direction"]

    dt_object1 = datetime.strptime(p_timestamp, "%Y-%m-%dT%H:%M:%S%z")
    out_rec.append(dt_object1.date())
    out_rec.append(months[dt_object1.month-1])
    out_rec.append(p_entry_price)
    out_rec.append(p_exit_candle[3])
    out_rec.append(direction[p_direction])
    out_rec.append(round(p_captured_points,2))
    out_rec.append(p_candle)
    f = open("./output/nifty.csv", "a")
    f.write(",".join(str(c) for c in out_rec))
    f.write("\n")
    f.close()