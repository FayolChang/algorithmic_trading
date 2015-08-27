# snp_forecast.py

import datetime

import pandas as pd
from sklearn.qda import QDA

from strategy import Strategy
from event import SignalEvent
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from equal_portfolio import EqualWeightedPortfolio
from create_lagged_series import create_lagged_series


class SPYDailyForecastStrategy(Strategy):
    """
    S&P500 forecast strategy. It uses a Quadratic Discriminant
    Analyser to predict the returns for a subsequent time
    period and then generated long/exit signals based on the
    prediction.
    """

    def __init__(self, bars, events):
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events

        self.strategy_id = '000001'
        self.datetime = datetime.datetime.utcnow()

        self.model_start_date = datetime.datetime(2001, 1, 10)
        self.model_end_date = datetime.datetime(2005, 12, 31)
        self.model_start_test_date = datetime.datetime(2005, 1, 1)

        self.long_market = False
        self.short_market = False
        self.bar_index = 0

        self.model = self.create_symbol_forecast_model()

    def create_symbol_forecast_model(self):
        # Create a lagged series of the S&P500 US stock market index
        snpret = create_lagged_series(
            self.symbol_list[0], self.model_start_date,
            self.model_end_date, lags=5
        )

        # Use the prior two days of returns as predictor
        # values, with direction as the response
        X = snpret[["Lag1", "Lag2"]]
        y = snpret["Direction"]

        # Create training and test sets
        start_test = self.model_start_test_date
        X_train = X[X.index < start_test]
        X_test = X[X.index >= start_test]
        y_train = y[y.index < start_test]
        y_test = y[y.index >= start_test]

        model = QDA()
        model.fit(X_train, y_train)
        return model

    def calculate_signals(self, event):
        """
        Calculate the SignalEvents based on market data.
        """
        sid = self.strategy_id
        sym = self.symbol_list[0]
        dt = self.datetime

        if event.type == 'BarArrive':
            self.bar_index += 1
            if self.bar_index > 5:
                lags = self.bars.get_latest_bars_values(
                    self.symbol_list[0], "returns", N=3
                )
                pred_series = pd.Series(
                    {
                        'Lag1': lags[1] * 100.0,
                        'Lag2': lags[2] * 100.0
                    }
                )
                pred = self.model.predict(pred_series)
                if pred > 0 and not self.long_market:
                    self.long_market = True
                    signal = SignalEvent(sid, sym, dt, 'LONG', 1.0)
                    self.events.put(signal)

                if pred < 0 and self.long_market:
                    self.long_market = False
                    signal = SignalEvent(sid, sym, dt, 'EXIT', 1.0)
                    self.events.put(signal)


if __name__ == "__main__":
    csv_dir = '/path/to/your/csv/data/'
    symbol_list = ['SPY']
    initial_capital = 100000.0
    periods = "D"
    start_date = datetime.datetime(2006, 1, 3)

    backtest = Backtest(
        csv_dir, symbol_list, initial_capital, start_date,
        HistoricCSVDataHandler, SimulatedExecutionHandler,
        EqualWeightedPortfolio, SPYDailyForecastStrategy,
        periods, header_format="yahoo", max_iters=None
    )
    backtest.simulate_trading()
