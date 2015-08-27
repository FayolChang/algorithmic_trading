# create_lagged_series.py

import datetime

import numpy as np
import pandas as pd
from pandas.io.data import DataReader


def create_lagged_series(symbol, start_date, end_date, lags=5):
    """
    This creates a pandas DataFrame that stores the 
    percentage returns of the adjusted closing value of 
    a stock obtained from Yahoo Finance, along with a 
    number of lagged returns from the prior trading days 
    (lags defaults to 5 days). Trading volume, as well as 
    the Direction from the previous day, are also included.
    """

    # Obtain stock information from Yahoo Finance
    ts = DataReader(
        symbol, "yahoo",
        start_date - datetime.timedelta(days=365),
        end_date
    )

    # Create the new lagged DataFrame
    ts_lag = pd.DataFrame(index=ts.index)
    ts_lag["Today"] = ts["Adj Close"]
    ts_lag["Volume"] = ts["Volume"]

    # Create the shifted lag series of prior trading period close values
    for i in xrange(0, lags):
        ts_lag["Lag%s" % str(i + 1)] = ts["Adj Close"].shift(i + 1)

    # Create the returns DataFrame
    ts_ret = pd.DataFrame(index=ts_lag.index)
    ts_ret["Volume"] = ts_lag["Volume"]
    ts_ret["Today"] = ts_lag["Today"].pct_change() * 100.0

    # If any of the values of percentage returns equal zero, set them to
    # a small number (stops issues with QDA model in scikit-learn)
    for i, x in enumerate(ts_ret["Today"]):
        if abs(x) < 0.0001:
            ts_ret["Today"][i] = 0.0001

    # Create the lagged percentage returns columns
    for i in xrange(0, lags):
        ts_ret["Lag%s" % str(i + 1)] = \
            ts_lag["Lag%s" % str(i + 1)].pct_change() * 100.0

    # Create the "Direction" column (+1 or -1) indicating an up/down day
    ts_ret["Direction"] = np.sign(ts_ret["Today"])
    ts_ret = ts_ret[ts_ret.index >= start_date]

    return ts_ret
