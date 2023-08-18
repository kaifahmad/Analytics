import os
import sys
from util import write_to_csv
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

# remove old file
os.remove("./output/nifty.csv") if os.path.exists("./output/nifty.csv") else None
COUNTER = 0
with open(
    "../../../Data-loader/output/nifty_60minute.csv", "r"
) as file:  # the a opens it in append mode
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
            #Exit criteria
            # @long
            if open_trade and trade_type == 0:
                max_intrade.append(candle[1])
                min_intrade.append(candle[2])
                if(candle[3] <= min(lows)):
                    exit_price = candle[3]
                    open_trade = False
                    write_to_csv(
                        p_in_timestamp = in_timestamp,
                        p_timestamp = line_data[0],
                        p_exit_candle = candle,
                        p_entry_price = in_price,
                        p_captured_points = exit_price - in_price,
                        p_direction = trade_type,
                        p_in_candle = in_candle,
                        p_candle = line_data[-3],
                        p_max_points = max(max_intrade) - in_price,
                        p_max_loss = min(min_intrade) - in_price
                    )
                    if (max(max_intrade) - in_price) > 50.0:
                        COUNTER += 1
            
            elif open_trade and trade_type == 1:
                max_intrade.append(candle[1])
                min_intrade.append(candle[2])
                if(candle[3] >= max(highs)):
                    exit_price = candle[3]
                    open_trade = False
                    write_to_csv(
                        p_in_timestamp = in_timestamp,
                        p_timestamp = line_data[0],
                        p_exit_candle = candle,
                        p_entry_price = in_price,
                        p_captured_points = in_price - exit_price,
                        p_direction = trade_type,
                        p_in_candle = in_candle,
                        p_candle = line_data[-3],
                        p_max_points = in_price - min(min_intrade),
                        p_max_loss = in_price - max(max_intrade)
                    )
                    if (in_price - min(min_intrade)) > 50.0:
                        COUNTER += 1

            #Entry criteria
            # @long
            if candle[3] >= max(highs) and not open_trade:
                open_trade = True
                trade_type = 0
                in_price = candle[3]
                in_timestamp = line_data[0]
                in_candle = line_data[-3]
                min_intrade = []
                max_intrade = []
            # @short
            elif candle[3] <= min(lows) and not open_trade:
                open_trade = True
                trade_type = 1
                in_price = candle[3]
                in_timestamp = line_data[0]
                in_candle = line_data[-3]
                min_intrade = []
                max_intrade = []

            # update the highs and lows
            highs.pop(0)
            highs.append(candle[1])
            lows.pop(0)
            lows.append(candle[2])
        except Exception as e:
            print(in_price,trade_type,candle,candle[3] - in_price)
            print(e)
            break

print(COUNTER)