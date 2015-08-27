import numpy as np
import pandas as pd


def create_cagr(equity, periods=252):
    """
    Calculates the Compound Annual Growth Rate (CAGR)
    for the portfolio, by determining the number of years
    and then creating a compound annualised rate based
    on the total return.

    Parameters:
    equity - A pandas Series representing the equity curve.
    periods - Daily (252), Hourly (252*6.5), Minutely(252*6.5*60) etc.
    """
    years = len(equity) / float(periods)
    return (equity[-1] ** (1.0 / years)) - 1.0


def create_sharpe_ratio(returns, periods=252):
    """
    Create the Sharpe ratio for the strategy, based on a 
    benchmark of zero (i.e. no risk-free rate information).

    Parameters:
    returns - A pandas Series representing period percentage returns.
    periods - Daily (252), Hourly (252*6.5), Minutely(252*6.5*60) etc.
    """
    return np.sqrt(periods) * (np.mean(returns)) / np.std(returns)


def create_drawdowns(pnl):
    """
    Calculate the largest peak-to-trough drawdown of the PnL curve
    as well as the duration of the drawdown. Requires that the 
    pnl_returns is a pandas Series.

    Parameters:
    pnl - A pandas Series representing period percentage returns.

    Returns:
    drawdown, duration - Highest peak-to-trough drawdown and duration.
    """

    # Calculate the cumulative returns curve
    # and set up the High Water Mark
    hwm = [0]

    # Create the drawdown and duration series
    idx = pnl.index
    drawdown = pd.Series(index=idx)
    duration = pd.Series(index=idx)

    # Loop over the index range
    for t in range(1, len(idx)):
        hwm.append(max(hwm[t - 1], pnl[t]))
        drawdown[t] = (hwm[t] - pnl[t])
        duration[t] = (0 if drawdown[t] == 0 else duration[t - 1] + 1)
    return drawdown, drawdown.max(), duration.max()
