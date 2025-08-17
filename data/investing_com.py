import investpy
import pandas as pd
from utils.logger import setup_logger
from datetime import datetime

logger = setup_logger()

class InvestingData:
    def fetch_ohlcv(self, symbol, timeframe='Daily', start_date=None, end_date=None):
        """
        Fetches historical OHLCV data from Investing.com.
        :param symbol: The ticker symbol (e.g., 'AAPL').
        :param timeframe: Data interval ('Daily', 'Weekly', 'Monthly').
        :param start_date: Start date string in DD/MM/YYYY format.
        :param end_date: End date string in DD/MM/YYYY format.
        """
        try:
            # investpy uses DD/MM/YYYY format
            start_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            end_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            
            logger.info(f"Fetching data for {symbol} from Investing.com...")
            data = investpy.get_stock_historical_data(
                stock=symbol,
                country='United States', # Assuming US stocks for now
                from_date=start_formatted,
                to_date=end_formatted,
                interval=timeframe
            )

            if data.empty:
                logger.warning(f"No data found for symbol {symbol}.")
                return []

            # Convert to the format expected by the backtester
            data = data.reset_index()
            data['timestamp'] = data['Date'].apply(lambda x: int(x.timestamp() * 1000))
            data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
            
            return data[['timestamp', 'open', 'high', 'low', 'close', 'volume']].values.tolist()
        except Exception as e:
            logger.error(f"Error fetching data from Investing.com for {symbol}: {e}")
            return []
