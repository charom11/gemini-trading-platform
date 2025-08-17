from utils.logger import setup_logger

logger = setup_logger()

class PaperTradingExchange:
    def __init__(self, real_exchange, initial_balance={'USDT': 10000}):
        """
        Initializes the paper trading exchange.
        :param real_exchange: An instance of a real exchange connector (e.g., BinanceExchange) for market data.
        :param initial_balance: A dictionary representing the starting balance.
        """
        self.real_exchange = real_exchange
        self.balance = initial_balance.copy()
        self.trades = []
        logger.info(f"Paper trading exchange initialized with balance: {self.balance}")

    def get_balance(self, currency='USDT'):
        return self.balance.get(currency, {'free': 0, 'used': 0, 'total': 0})

    def get_ticker(self, symbol):
        # Fetches real market data
        return self.real_exchange.get_ticker(symbol)

    def fetch_ohlcv(self, symbol, timeframe='1h', limit=100):
        # Fetches real historical data
        return self.real_exchange.fetch_ohlcv(symbol, timeframe, limit)

    def create_order(self, symbol, order_type, side, amount, price=None):
        logger.info(f"PAPER TRADE: Received {side} order for {amount} {symbol.split('/')[0]} at price {price or 'market'}")
        
        base_currency, quote_currency = symbol.split('/')
        
        # Get the current market price for the simulation
        if price is None:
            ticker = self.get_ticker(symbol)
            if not ticker:
                logger.error("PAPER TRADE: Could not fetch ticker for market price. Order failed.")
                return None
            price = ticker['last']

        cost = amount * price

        # Ensure currencies exist in balance
        if base_currency not in self.balance:
            self.balance[base_currency] = {'free': 0, 'used': 0, 'total': 0}
        if quote_currency not in self.balance:
            self.balance[quote_currency] = {'free': 0, 'used': 0, 'total': 0}

        # --- Simulate the trade ---
        if side == 'buy':
            if self.balance[quote_currency]['free'] >= cost:
                self.balance[quote_currency]['free'] -= cost
                self.balance[quote_currency]['total'] -= cost
                self.balance[base_currency]['free'] += amount
                self.balance[base_currency]['total'] += amount
                
                trade = {'symbol': symbol, 'side': side, 'amount': amount, 'price': price, 'cost': cost}
                self.trades.append(trade)
                logger.info(f"PAPER TRADE: Executed BUY order for {amount} {base_currency} at {price}. Cost: {cost} {quote_currency}")
                return trade
            else:
                logger.warning("PAPER TRADE: Insufficient funds to execute BUY order.")
                return None
        
        elif side == 'sell':
            if self.balance[base_currency]['free'] >= amount:
                self.balance[base_currency]['free'] -= amount
                self.balance[base_currency]['total'] -= amount
                self.balance[quote_currency]['free'] += cost
                self.balance[quote_currency]['total'] += cost

                trade = {'symbol': symbol, 'side': side, 'amount': amount, 'price': price, 'cost': cost}
                self.trades.append(trade)
                logger.info(f"PAPER TRADE: Executed SELL order for {amount} {base_currency} at {price}. Gained: {cost} {quote_currency}")
                return trade
            else:
                logger.warning("PAPER TRADE: Insufficient funds to execute SELL order.")
                return None
        
        return None
