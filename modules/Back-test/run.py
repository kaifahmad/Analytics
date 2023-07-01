import os
from util import write_to_csv

open_trade: bool = False
trade_type = 0
in_price = 0
net_points_captured = 0

if not os.path.exists("./output"):
    os.mkdir("./output")

# remove old file
os.remove("./output/nifty.csv") if os.path.exists("./output/nifty.csv") else None

with open(
    "../Data-loader/output/nifty.csv", "r"
) as file:  # the a opens it in append mode
    while True:
        try:
            line = next(file).strip("\r\n")
            line_data = line.split(",")
            candle = [
                float(line_data[1]),
                float(line_data[2]),
                float(line_data[3]),
                float(line_data[4]),
            ]
            if not open_trade and line_data[-3] == "T15_0":
                if float(line_data[-1]) >= 0:
                    open_trade = True
                    trade_type = 0
                    in_price = float(line_data[4])
                else:
                    open_trade = True
                    trade_type = 1
                    in_price = float(line_data[4])
            elif line_data[-3] != "T9_15" and open_trade:
                # skipping if its the first candle
                if candle[3] < prevCandle[2] and trade_type == 0:
                    # exit
                    ex_price = candle[3]
                    open_trade = False
                    write_to_csv(
                        p_timestamp = line_data[0],
                        p_exit_candle = candle, 
                        p_entry_price = in_price,
                        p_captured_points = ex_price - in_price,
                        p_direction = trade_type
                    )
                elif (candle[3] > prevCandle[1] and trade_type == 1) or line_data[-3] != "T14_45":
                    # exit
                    ex_price = candle[3]
                    open_trade = False
                    write_to_csv(
                        p_timestamp = line_data[0],
                        p_exit_candle = candle, 
                        p_entry_price = in_price,
                        p_captured_points=in_price - ex_price,
                        p_direction = trade_type
                    )

            prevCandle = candle

        except Exception as e:
            print(e)
            break
        print(line)
