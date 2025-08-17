import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exchanges.binance import BinanceExchange
from config.settings import BINANCE_API_KEY, BINANCE_API_SECRET
from utils.logger import setup_logger

logger = setup_logger()

def test_binance_connection():
    logger.info("Testing Binance exchange connection...")
    try:
        exchange = BinanceExchange(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

        # Test get_balance
        balance = exchange.get_balance('USDT')
        if balance:
            logger.info(f"Successfully fetched USDT balance: {balance}")
        else:
            logger.warning("Could not fetch USDT balance or it is zero.")

        # Test get_ticker
        ticker = exchange.get_ticker('BTC/USDT')
        if ticker:
            logger.info(f"Successfully fetched BTC/USDT ticker: {ticker['last']}")
        else:
            logger.warning("Could not fetch BTC/USDT ticker.")

    except Exception as e:
        logger.error(f"An error occurred during the Binance connection test: {e}")

if __name__ == "__main__":
    test_binance_connection()
