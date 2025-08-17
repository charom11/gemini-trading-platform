import pandas as pd

def calculate_atr(data, period=14):
    """
    Calculates the Average True Range (ATR).
    """
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    else:
        df = data

    if 'high' not in df.columns or len(df) < period:
        return None

    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr.iloc[-1]
