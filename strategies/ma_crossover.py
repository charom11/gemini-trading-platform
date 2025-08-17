from utils.logger import setup_logger
from signals.moving_average import calculate_moving_average

logger = setup_logger()

class MovingAverageCrossoverStrategy:
    def __init__(self, symbol, config, on_trade):
        self.symbol = symbol
        self.config = config
        self.on_trade = on_trade
        self.fast_period = self.config.get('fast_period', 20)
        self.slow_period = self.config.get('slow_period', 50)
        self.last_signal = None # To track the crossover state

    def execute(self, data, current_equity=None):
        """
        Executes the strategy on a slice of historical data.
        """
        current_price = data['close'].iloc[-1]
        current_timestamp = data.index[-1]
        
        # Calculate signals
        fast_ma = calculate_moving_average(data, self.fast_period)
        slow_ma = calculate_moving_average(data, self.slow_period)

        if fast_ma is None or slow_ma is None:
            return # Not enough data yet

        logger.debug(f"[{current_timestamp}] Price: {current_price:.2f}, Fast MA: {fast_ma:.2f}, Slow MA: {slow_ma:.2f}")

        # --- Trading Logic (Crossover) ---
        if fast_ma > slow_ma and self.last_signal != 'buy':
            logger.info(f"[{current_timestamp}] Fast MA crossed above Slow MA. Executing BUY.")
            self.on_trade('buy', 0.1, current_price, current_timestamp)
            self.last_signal = 'buy'
        elif fast_ma < slow_ma and self.last_signal != 'sell':
            logger.info(f"[{current_timestamp}] Fast MA crossed below Slow MA. Executing SELL.")
            self.on_trade('sell', 0.1, current_price, current_timestamp)
            self.last_signal = 'sell'
