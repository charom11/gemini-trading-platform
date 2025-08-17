from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from utils.logger import setup_logger
import pandas as pd

logger = setup_logger()

class AlpacaExchange:
    def __init__(self, api_key, api_secret, paper=True):
        try:
            self.trading_client = TradingClient(api_key, api_secret, paper=paper)
            self.data_client = StockHistoricalDataClient(api_key, api_secret)
            account = self.trading_client.get_account()
            logger.info(f"Alpaca connection successful. Account: {account.account_number}")
        except Exception as e:
            logger.error(f"Alpaca authentication failed: {e}")
            raise

    def fetch_ohlcv(self, symbol, timeframe='1d', start_date=None, end_date=None):
        timeframe_map = {
            '1h': TimeFrame.Hour,
            '1d': TimeFrame.Day,
        }
        alpaca_timeframe = timeframe_map.get(timeframe, TimeFrame.Day)
        try:
            request_params = StockBarsRequest(
                symbol_or_symbols=[symbol],
                timeframe=alpaca_timeframe,
                start=start_date,
                end=end_date
            )
            bars = self.data_client.get_stock_bars(request_params).df
            bars = bars.reset_index()
            bars['timestamp'] = bars['timestamp'].apply(lambda x: int(x.timestamp() * 1000))
            bars.rename(columns={'symbol': 'symbol_col'}, inplace=True)
            return bars[['timestamp', 'open', 'high', 'low', 'close', 'volume']].values.tolist()
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {symbol} from Alpaca: {e}")
            return []
