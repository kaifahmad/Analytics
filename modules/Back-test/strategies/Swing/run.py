from logging import Logger
import os
import sys
from util import write_to_csv
open_trade: bool = False
trade_type = 0
in_price = 0
exit_price = 0
net_points_captured = 0
lows:list = [sys.float_info.min,sys.float_info.min,sys.float_info.min,sys.float_info.min]
highs:list = [sys.float_info.max,sys.float_info.max,sys.float_info.max,sys.float_info.max]

if not os.path.exists("./output"):
    os.mkdir("./output")

# remove old file
os.remove("./output/nifty.csv") if os.path.exists("./output/nifty.csv") else None

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
                if(candle[3] <= min(lows)):
                    exit_price = candle[3]
                    open_trade = False
                    write_to_csv(
                        p_timestamp = line_data[0],
                        p_exit_candle = candle,
                        p_entry_price = in_price,
                        p_captured_points = exit_price - in_price,
                        p_direction = trade_type,
                        p_candle = line_data[-3]
                    )
            
            if open_trade and trade_type == 1:
                if(candle[3] >= max(highs)):
                    exit_price = candle[3]
                    open_trade = False
                    write_to_csv(
                        p_timestamp = line_data[0],
                        p_exit_candle = candle,
                        p_entry_price = in_price,
                        p_captured_points = in_price - exit_price,
                        p_direction = trade_type,
                        p_candle = line_data[-3]
                    )

            #Entry criteria
            # @long
            if candle[3] >= max(highs) and not open_trade:
                open_trade = True
                trade_type = 0
                in_price = candle[3]
            # @short
            elif candle[3] <= min(lows) and not open_trade:
                open_trade = True
                trade_type = 1
                in_price = candle[3]


            # update the highs and lows
            highs.pop(0)
            highs.append(candle[1])
            highs.pop(0)
            lows.append(candle[2])
        except Exception as e:
            print(e)
