from utils.logger import setup_logger
import numpy as np

logger = setup_logger()

class GridStrategy:
    def __init__(self, symbol, config, on_trade):
        self.symbol = symbol
        self.config = config
        self.on_trade = on_trade
        self.grid_levels = self.config.get('levels', 10)
        self.quantity = self.config.get('quantity', 0.1)
        self.grid_initialized = False
        self.grid_lines = []
        self.last_crossed_line = None

    def initialize_grid(self, current_price):
        logger.info(f"Initializing grid for {self.symbol} around price {current_price}")
        price_range = current_price * 0.10 # 10% range around the starting price
        self.grid_lines = np.linspace(current_price - price_range, current_price + price_range, self.grid_levels)
        self.grid_initialized = True

    def execute(self, data, current_equity=None):
        current_price = data['close'].iloc[-1]
        current_timestamp = data.index[-1]

        if not self.grid_initialized:
            self.initialize_grid(current_price)
            return

        # Find which grid cell the current price is in
        for i in range(len(self.grid_lines) - 1):
            if self.grid_lines[i] <= current_price < self.grid_lines[i+1]:
                current_line_index = i
                
                # If we have crossed a new line, execute a trade
                if self.last_crossed_line is not None and current_line_index != self.last_crossed_line:
                    # Moving up past a grid line is a sell signal (selling higher)
                    if current_line_index > self.last_crossed_line:
                        logger.info(f"[{current_timestamp}] Price crossed UP to {current_price:.2f}. Executing SELL.")
                        self.on_trade('sell', self.quantity, current_price, current_timestamp)
                    # Moving down past a grid line is a buy signal (buying lower)
                    else:
                        logger.info(f"[{current_timestamp}] Price crossed DOWN to {current_price:.2f}. Executing BUY.")
                        self.on_trade('buy', self.quantity, current_price, current_timestamp)
                
                self.last_crossed_line = current_line_index
                break
