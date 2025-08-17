import pandas as pd

def calculate_rsi(data, period=14):
    """
    Calculates the Relative Strength Index (RSI).
    
    :param data: List of lists (OHLCV) or pandas DataFrame.
    :param period: The period for the RSI calculation.
    :return: The latest RSI value, or None if calculation is not possible.
    """
    if not isinstance(data, pd.DataFrame):
        # Assuming data is in OHLCV format from ccxt
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    else:
        df = data

    if 'close' not in df.columns or len(df) < period:
        return None

    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi.iloc[-1]
