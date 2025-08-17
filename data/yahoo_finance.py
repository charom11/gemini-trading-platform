import yfinance as yf
import pandas as pd
from utils.logger import setup_logger
import time

logger = setup_logger()

class YahooFinanceData:
    def fetch_ohlcv(self, symbol, timeframe='1d', start_date=None, end_date=None):
        """
        Fetches historical OHLCV data from Yahoo Finance with retries.
        """
        for i in range(3): # Retry up to 3 times
            try:
                logger.info(f"Fetching data for {symbol} from Yahoo Finance (Attempt {i+1})...")
                ticker = yf.Ticker(symbol)
                data = ticker.history(start=start_date, end=end_date, interval=timeframe)
                
                if data.empty:
                    logger.warning(f"No data found for symbol {symbol} in the given date range.")
                    time.sleep(1) # Wait before retrying
                    continue

                # Convert to the format expected by the backtester
                data = data.reset_index()
                data['timestamp'] = data.iloc[:, 0].apply(lambda x: int(x.timestamp() * 1000))
                data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
                
                return data[['timestamp', 'open', 'high', 'low', 'close', 'volume']].values.tolist()
            except Exception as e:
                logger.error(f"Error fetching data from Yahoo Finance for {symbol}: {e}")
                time.sleep(2) # Wait longer on error
        
        logger.error(f"Failed to fetch data for {symbol} after multiple attempts.")
        return []
