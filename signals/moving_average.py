import pandas as pd

def calculate_moving_average(data, period=50):
    """
    Calculates the Simple Moving Average (SMA).
    
    :param data: List of lists (OHLCV) or pandas DataFrame.
    :param period: The period for the SMA calculation.
    :return: The latest SMA value, or None.
    """
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    else:
        df = data

    if 'close' not in df.columns or len(df) < period:
        return None

    sma = df['close'].rolling(window=period).mean()
    
    return sma.iloc[-1]
