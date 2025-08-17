from utils.logger import setup_logger
from signals.macd import calculate_macd

logger = setup_logger()

class MomentumStrategy:
    def __init__(self, symbol, config, on_trade):
        self.symbol = symbol
        self.config = config
        self.on_trade = on_trade
        self.last_signal = None # To avoid repeated signals

    def execute(self, data):
        """
        Executes the strategy on a slice of historical data.
        """
        current_price = data['close'].iloc[-1]
        current_timestamp = data.index[-1]

        # Calculate the signal
        macd_line, signal_line = calculate_macd(data)
        if macd_line is None or signal_line is None:
            return

        logger.debug(f"[{current_timestamp}] Price: {current_price:.2f}, MACD: {macd_line:.2f}, Signal: {signal_line:.2f}")

        # --- Trading Logic (MACD Crossover) ---
        # We use a simplified portfolio that only holds one position at a time,
        # so we only need to check for buy signals. The engine handles exits.
        if macd_line > signal_line and self.last_signal != 'buy':
            logger.info(f"[{current_timestamp}] MACD crossover signal. Executing BUY.")
            # The quantity is now fixed for simplicity, but could be dynamic
            self.on_trade('buy', 0.1, current_price, current_timestamp)
            self.last_signal = 'buy'
        elif macd_line < signal_line:
            # If the signal flips to sell, we reset our 'last_signal' so we're ready to buy again
            self.last_signal = 'sell'
