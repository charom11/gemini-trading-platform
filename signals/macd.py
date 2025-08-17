import pandas as pd

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculates the Moving Average Convergence Divergence (MACD).
    
    :param data: List of lists (OHLCV) or pandas DataFrame.
    :param fast_period: The period for the fast EMA.
    :param slow_period: The period for the slow EMA.
    :param signal_period: The period for the signal line EMA.
    :return: A tuple of (latest MACD line, latest Signal line), or (None, None).
    """
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    else:
        df = data

    if 'close' not in df.columns or len(df) < slow_period:
        return None, None

    # Calculate the Fast and Slow EMAs
    fast_ema = df['close'].ewm(span=fast_period, adjust=False).mean()
    slow_ema = df['close'].ewm(span=slow_period, adjust=False).mean()

    # Calculate the MACD line
    macd_line = fast_ema - slow_ema

    # Calculate the Signal line
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    return macd_line.iloc[-1], signal_line.iloc[-1]
