def write_to_csv(p_exit_candle: list, p_captured_points):
    """
    Writes the outcome to the csv file
    """
    p_exit_candle.append(p_captured_points)
    f = open("./output/nifty.csv", "a")
    f.write(",".join(str(c) for c in p_exit_candle))
    f.write("\n")
    f.close()