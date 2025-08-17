import time
from utils.logger import setup_logger

logger = setup_logger()

class TradingEngine:
    def __init__(self, strategy, exchange, mode, symbol):
        self.strategy = strategy
        self.exchange = exchange
        self.mode = mode
        self.symbol = symbol
        self.is_running = True

    def run(self):
        logger.info(f"Starting trading engine in {self.mode} mode for {self.symbol}.")
        while self.is_running:
            try:
                # Fetch the latest market data
                ticker = self.exchange.get_ticker(self.symbol)
                if ticker:
                    # Execute the trading strategy
                    self.strategy.execute(ticker)
                
                # Wait for the next interval
                time.sleep(5) # TODO: Make this configurable
            except KeyboardInterrupt:
                self.is_running = False
                logger.info("Trading bot stopped by user.")
            except Exception as e:
                logger.error(f"An error occurred in the trading loop: {e}")
                # Optional: add a longer sleep time on error to prevent spamming
                time.sleep(60)

    def stop(self):
        self.is_running = False
