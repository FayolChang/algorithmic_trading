from math import floor

from portfolio import Portfolio
from event import OrderEvent


class EqualWeightedPortfolio(Portfolio):
    """
    The EqualWeightedPortfolio object is designed to send orders to
    a brokerage object with a size based on strategy equal weight
    allocation. The number of strategies are determined at initialisation
    and orders are sent using quantity that grows with the size of
    the account.
    """

    def __init__(
            self, bars, events, start_date, num_strategy,
            periods="D", initial_capital=100000.0
    ):
        """
        Initialises the portfolio with bars and an event queue. 
        Also includes a starting datetime index and initial capital 
        (USD unless otherwise stated).

        Parameters:
        bars - The DataHandler object with current market data.
        events - The Event Queue object.
        start_date - The start date (bar) of the portfolio.
        num_strategy - The number of strategies to split capital across.
        periods - D, H, M or S depending on daily, hourly, minutely or secondly.
        initial_capital - The starting capital in USD.
        """
        super(EqualWeightedPortfolio, self).__init__(
            bars, events, start_date, periods, initial_capital
        )
        self.num_strats = num_strategy
        self.port_split = 1.0 / num_strategy

    def generate_equal_weighted_order(self, signal):
        """
        Simply files an Order object as a constant quantity
        sizing of the signal object, without risk management or
        position sizing considerations.

        Parameters:
        signal - The tuple containing Signal information.
        """
        order = None

        symbol = signal.symbol
        direction = signal.signal_type
        strength = signal.strength

        cash = self.current_holdings['cash']
        mkt_price = self.bars.get_latest_bar_value(symbol, "close")
        allocation = 100

        mkt_quantity = floor(allocation * strength)
        cur_quantity = self.current_positions[symbol]
        order_type = 'MKT'

        if direction == 'LONG' and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY')
        if direction == 'SHORT' and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'SELL')

        if direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'SELL')
        if direction == 'EXIT' and cur_quantity < 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'BUY')
        return order

    def update_signal(self, event):
        """
        Acts on a SignalEvent to generate new orders 
        based on the portfolio logic.
        """
        if event.type == 'SIGNAL':
            order_event = self.generate_equal_weighted_order(event)
            self.events.put(order_event)
