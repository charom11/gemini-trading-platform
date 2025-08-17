from utils.logger import setup_logger
from signals.macd import calculate_macd
from signals.atr import calculate_atr

logger = setup_logger()

class MomentumATRStrategy:
    def __init__(self, symbol, config, on_trade):
        self.symbol = symbol
        self.config = config
        self.on_trade = on_trade
        self.last_signal = None
        self.current_atr = 0

    def execute(self, data, current_equity):
        current_price = data['close'].iloc[-1]
        current_timestamp = data.index[-1]

        # Calculate indicators
        macd_line, signal_line = calculate_macd(data)
        self.current_atr = calculate_atr(data, period=self.config.get('atr_period', 14))

        if macd_line is None or signal_line is None or self.current_atr is None:
            return

        # --- Position Sizing (Risk 2% of equity per trade) ---
        risk_per_trade = 0.02 * current_equity
        stop_loss_distance = self.current_atr * self.config.get('atr_multiplier', 2.0)
        if stop_loss_distance == 0: return # Avoid division by zero
        position_size = risk_per_trade / stop_loss_distance

        # --- Trading Logic ---
        if macd_line > signal_line and self.last_signal != 'buy':
            logger.info(f"[{current_timestamp}] MACD crossover BUY signal. Sizing for {position_size:.4f} units.")
            self.on_trade('buy', position_size, current_price, current_timestamp)
            self.last_signal = 'buy'
        elif macd_line < signal_line:
            self.last_signal = 'sell'
