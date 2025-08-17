from utils.logger import setup_logger

logger = setup_logger()

class Portfolio:
    def __init__(self, initial_cash=10000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {} # { 'symbol': {'quantity': float, 'entry_price': float} }
        self.trades = []
        logger.info(f"Portfolio initialized with ${self.initial_cash:.2f} cash.")

    def execute_trade(self, timestamp, symbol, side, quantity, price):
        """Simulates the execution of a trade and updates the portfolio."""
        cost = quantity * price
        
        if side == 'buy':
            if self.cash < cost:
                logger.warning(f"Not enough cash to execute buy for {quantity} {symbol} at ${price:.2f}")
                return
            
            self.cash -= cost
            # A simple portfolio that only holds one position at a time
            if symbol in self.positions:
                logger.warning(f"Already holding a position in {symbol}. Ignoring new buy signal.")
                return
            self.positions[symbol] = {'quantity': quantity, 'entry_price': price}

        elif side == 'sell':
            if symbol not in self.positions:
                logger.warning(f"No position to sell for {symbol}")
                return
            
            self.cash += cost
            del self.positions[symbol]

        trade = {
            'timestamp': timestamp,
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price,
            'cost': cost
        }
        self.trades.append(trade)
        logger.debug(f"Executed trade: {trade}")

    def get_total_equity(self, current_prices):
        """Calculates the total current value (equity) of the portfolio."""
        total_value = self.cash
        for symbol, position in self.positions.items():
            total_value += position['quantity'] * current_prices.get(symbol, 0)
        return total_value
