import ccxt
from utils.logger import setup_logger

logger = setup_logger()

class BinanceExchange:
    def __init__(self, api_key, api_secret):
        try:
            self.exchange = ccxt.binance({
                'apiKey': api_key,
                'secret': api_secret,
            })
            self.exchange.load_markets()
            logger.info("Binance exchange initialized successfully.")
        except ccxt.AuthenticationError as e:
            logger.error(f"Binance authentication failed: {e}")
            raise
        except ccxt.BaseError as e:
            logger.error(f"An error occurred with Binance exchange: {e}")
            raise

    def get_balance(self, currency='USDT'):
        try:
            balance = self.exchange.fetch_balance()
            if currency in balance:
                return balance[currency]
            return None
        except ccxt.BaseError as e:
            logger.error(f"Error fetching balance: {e}")
            return None

    def get_ticker(self, symbol):
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except ccxt.BaseError as e:
            logger.error(f"Error fetching ticker for {symbol}: {e}")
            return None

    def create_order(self, symbol, order_type, side, amount, price=None):
        try:
            order = self.exchange.create_order(symbol, order_type, side, amount, price)
            logger.info(f"Created order: {order}")
            return order
        except ccxt.BaseError as e:
            logger.error(f"Error creating order: {e}")
            return None

    def fetch_ohlcv(self, symbol, timeframe='1h', start_date=None, end_date=None):
        """
        Fetches historical OHLCV data from Binance, handling pagination for long date ranges.
        """
        from datetime import datetime, timezone
        import time

        try:
            since = int(datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp() * 1000)
            end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp() * 1000)
            limit = 1000
            all_ohlcv = []

            logger.info(f"Starting paginated fetch for {symbol} from {start_date} to {end_date}")

            while since < end_ts:
                logger.info(f"Fetching chunk for {symbol} starting from {datetime.fromtimestamp(since/1000)}...")
                ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
                if not ohlcv:
                    break # No more data available
                
                all_ohlcv.extend(ohlcv)
                since = ohlcv[-1][0] + 1 # Set the 'since' for the next request to the timestamp of the last candle
                
                # Be respectful of the API rate limit
                time.sleep(self.exchange.rateLimit / 1000)

            logger.info(f"Finished fetching. Total candles retrieved: {len(all_ohlcv)}")
            return all_ohlcv

        except ccxt.BaseError as e:
            logger.error(f"Error fetching OHLCV data for {symbol}: {e}")
            return []
