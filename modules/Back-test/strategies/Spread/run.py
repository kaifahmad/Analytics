import os
import sys
# from util import write_to_csv
open_trade: bool = False
trade_type = 0
in_price = 0
exit_price = 0
in_timestamp = ""
in_candle = ""
max_intrade = []
min_intrade = []

net_points_captured = 0
lows:list = [sys.float_info.min,sys.float_info.min,sys.float_info.min,sys.float_info.min]
highs:list = [sys.float_info.max,sys.float_info.max,sys.float_info.max,sys.float_info.max]
max(highs)

if not os.path.exists("./output"):
    os.mkdir("./output")

# remove old output file
os.remove("./output/nifty.csv") if os.path.exists("./output/nifty.csv") else None

WEEKADAY_DICT = {
    "0": "MONDAY",
    "1": "TUESDAY",
    "2": "WEDNESDAY",
    "3": "THURSDAY",
    "4": "FRIDAY"
}
prev_close = 0
in_trade: bool = False 
in_price = 0
direction = ""
total_trades = 0
loss_trades = 0
with open("data/nifty_day.csv", "r") as file:
    while True:
        try:
            line = next(file).strip("\r\n")
            line_data = line.split(",")
            candle = [
                float(line_data[1]),    #0	OPEN
                float(line_data[2]),    #1	HIGH 
                float(line_data[3]),    #2	LOW
                float(line_data[4]),    #3	CLOSE
            ]
            net_return = float(line_data[-1])
            day = line_data[-4]
            if int(day) == 1: # Entry on Tuesday day end
                in_trade = True
                total_trades +=1
                if candle[-1] - prev_close+10>= 0:
                    direction = "LONG"
                else:
                    direction = "SHORT"
                in_price = candle[-1]
            if in_trade and int(day) == 3:  # Exit on Wednseday day end
                if direction == "SHORT" and candle[-1] >= 1.01*in_price:
                    loss_trades += 1
                    print(f"Date: {line_data[-5]} , Day: {WEEKADAY_DICT[day]}, Direction: {direction}")
                elif direction == "LONG" and candle[-1] <= 0.990*in_price:
                    loss_trades += 1
                    print(f"Date: {line_data[-5]} , Day: {WEEKADAY_DICT[day]}, Direction: {direction}")
                in_trade = False
            if in_trade and int(day) == 4:
                in_trade = False
            if in_trade and int(day) == 0:
                in_trade = False
        except Exception as e:
            print(f"Exception ==> {line}")
            break
        prev_close = candle[-1]


print(f"Total: {total_trades}")
print(f"LOSS: {loss_trades}")
