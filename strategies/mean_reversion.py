from utils.logger import setup_logger
from signals.rsi import calculate_rsi

logger = setup_logger()

class MeanReversionStrategy:
    def __init__(self, symbol, config, on_trade):
        self.symbol = symbol
        self.config = config
        self.on_trade = on_trade # Callback to execute a trade
        self.oversold_threshold = self.config.get('oversold_threshold', 30)
        self.overbought_threshold = self.config.get('overbought_threshold', 70)
        self.last_signal = None

    def execute(self, data, current_equity=None):
        """
        Executes the strategy on a slice of historical data.
        :param data: Pandas DataFrame with historical OHLCV data.
        """
        current_price = data['close'].iloc[-1]
        current_timestamp = data.index[-1]
        
        # Calculate the signal
        rsi = calculate_rsi(data)
        if rsi is None:
            return

        logger.debug(f"[{current_timestamp}] Price: {current_price:.2f}, RSI: {rsi:.2f}")

        # --- Trading Logic ---
        if rsi < self.oversold_threshold and self.last_signal != 'buy':
            logger.info(f"[{current_timestamp}] Oversold signal. Executing BUY.")
            self.on_trade('buy', 0.1, current_price, current_timestamp) # Buy 0.1 units
            self.last_signal = 'buy'
        elif rsi > self.overbought_threshold and self.last_signal != 'sell':
            logger.info(f"[{current_timestamp}] Overbought signal. Executing SELL.")
            self.on_trade('sell', 0.1, current_price, current_timestamp) # Sell 0.1 units
            self.last_signal = 'sell'
