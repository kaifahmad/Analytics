open_trade: bool = False
trade_type = 0 
with open("../Data-loader/output/nifty.csv", "r") as file:  # the a opens it in append mode
    while True:
        try:
            line = next(file).strip("\r\n")
            line_data = line.split(',')
            if not open_trade and line_data[-3] == "T15_0":
                if float(line_data[-3]) >= 0:
                    """
                    Continue from here
                    """

                


        except Exception as e:
            break
        print(line)