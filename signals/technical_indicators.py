"""
Additional Technical Indicators for Enhanced ML Features
"""

import pandas as pd
import numpy as np
from typing import Tuple

def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate Bollinger Bands
    
    Args:
        df: DataFrame with 'close' column
        period: Period for moving average (default: 20)
        std_dev: Standard deviation multiplier (default: 2.0)
    
    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    middle = df['close'].rolling(window=period).mean()
    std = df['close'].rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    
    return upper, middle, lower

def calculate_stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
    """
    Calculate Stochastic Oscillator
    
    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        k_period: Period for %K calculation (default: 14)
        d_period: Period for %D calculation (default: 3)
    
    Returns:
        Tuple of (%K, %D)
    """
    lowest_low = df['low'].rolling(window=k_period).min()
    highest_high = df['high'].rolling(window=k_period).max()
    
    k_percent = 100 * ((df['close'] - lowest_low) / (highest_high - lowest_low))
    d_percent = k_percent.rolling(window=d_period).mean()
    
    return k_percent, d_percent

def calculate_williams_r(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Williams %R
    
    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        period: Period for calculation (default: 14)
    
    Returns:
        Williams %R series
    """
    highest_high = df['high'].rolling(window=period).max()
    lowest_low = df['low'].rolling(window=period).min()
    
    williams_r = -100 * ((highest_high - df['close']) / (highest_high - lowest_low))
    
    return williams_r

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate Average True Range
    
    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        period: Period for ATR calculation (default: 14)
    
    Returns:
        ATR series
    """
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
    atr = true_range.rolling(window=period).mean()
    
    return atr

def calculate_cci(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    Calculate Commodity Channel Index
    
    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        period: Period for CCI calculation (default: 20)
    
    Returns:
        CCI series
    """
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    sma = typical_price.rolling(window=period).mean()
    mean_deviation = typical_price.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())))
    
    cci = (typical_price - sma) / (0.015 * mean_deviation)
    
    return cci

def calculate_momentum(df: pd.DataFrame, period: int = 10) -> pd.Series:
    """
    Calculate Momentum indicator
    
    Args:
        df: DataFrame with 'close' column
        period: Period for momentum calculation (default: 10)
    
    Returns:
        Momentum series
    """
    momentum = df['close'] - df['close'].shift(period)
    return momentum

def calculate_rate_of_change(df: pd.DataFrame, period: int = 10) -> pd.Series:
    """
    Calculate Rate of Change
    
    Args:
        df: DataFrame with 'close' column
        period: Period for ROC calculation (default: 10)
    
    Returns:
        ROC series
    """
    roc = ((df['close'] - df['close'].shift(period)) / df['close'].shift(period)) * 100
    return roc

def calculate_volume_sma(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    Calculate Volume Simple Moving Average
    
    Args:
        df: DataFrame with 'volume' column
        period: Period for SMA calculation (default: 20)
    
    Returns:
        Volume SMA series
    """
    volume_sma = df['volume'].rolling(window=period).mean()
    return volume_sma

def calculate_price_volume_trend(df: pd.DataFrame) -> pd.Series:
    """
    Calculate Price Volume Trend
    
    Args:
        df: DataFrame with 'close' and 'volume' columns
    
    Returns:
        PVT series
    """
    price_change = df['close'].pct_change()
    pvt = (price_change * df['volume']).cumsum()
    return pvt

def calculate_obv(df: pd.DataFrame) -> pd.Series:
    """
    Calculate On Balance Volume
    
    Args:
        df: DataFrame with 'close' and 'volume' columns
    
    Returns:
        OBV series
    """
    obv = pd.Series(index=df.index, dtype=float)
    obv.iloc[0] = df['volume'].iloc[0]
    
    for i in range(1, len(df)):
        if df['close'].iloc[i] > df['close'].iloc[i-1]:
            obv.iloc[i] = obv.iloc[i-1] + df['volume'].iloc[i]
        elif df['close'].iloc[i] < df['close'].iloc[i-1]:
            obv.iloc[i] = obv.iloc[i-1] - df['volume'].iloc[i]
        else:
            obv.iloc[i] = obv.iloc[i-1]
    
    return obv