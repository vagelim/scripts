#!/usr/bin/env python
import datetime


def text_to_occ(option):
    """Takes an option in text format, returns option in OCC format."""
    # https://web.archive.org/web/20200622191119/https://help.yahoo.com/kb/SLN13884.html
    ticker, month, day, year, strike, option_type = option.split(" ")
    datetime_object = datetime.datetime.strptime(month, "%b")
    numerical_month = datetime_object.month

    strike = int(float(strike) * 1000)
    normalized_strike = f"{strike:08}"
    output = (
        f"{ticker}{year[2:]}{numerical_month}{day}{option_type[0]}{normalized_strike}"
    )
    print(output)
    return output


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        text_to_occ(sys.argv[1])
    else:
        print(f"\tUsage: {sys.argv[0]} 'SPY Jun 26 2020 300.0 Put'")
