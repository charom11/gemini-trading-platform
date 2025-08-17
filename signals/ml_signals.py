import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from signals.rsi import calculate_rsi
from signals.macd import calculate_macd
from signals.moving_average import calculate_moving_average
from signals.technical_indicators import (
    calculate_bollinger_bands, calculate_stochastic, calculate_williams_r,
    calculate_atr, calculate_cci, calculate_momentum, calculate_rate_of_change,
    calculate_volume_sma, calculate_price_volume_trend, calculate_obv
)
from utils.logger import setup_logger

logger = setup_logger()

def create_features(data):
    """
    Creates enhanced features from the historical data for the ML model.
    """
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # --- Basic Technical Indicators ---
    df['rsi'] = calculate_rsi(df)
    df['macd'], df['macd_signal'] = calculate_macd(df)
    df['sma_fast'] = calculate_moving_average(df, period=20)
    df['sma_slow'] = calculate_moving_average(df, period=50)
    
    # --- Enhanced Technical Indicators ---
    df['ema_12'] = df['close'].ewm(span=12).mean()
    df['ema_26'] = df['close'].ewm(span=26).mean()
    
    # Bollinger Bands
    bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(df)
    df['bb_upper'] = bb_upper
    df['bb_middle'] = bb_middle
    df['bb_lower'] = bb_lower
    df['bb_width'] = (bb_upper - bb_lower) / bb_middle  # Bollinger Band Width
    df['bb_position'] = (df['close'] - bb_lower) / (bb_upper - bb_lower)  # Price position within BB
    
    # Stochastic
    stoch_k, stoch_d = calculate_stochastic(df)
    df['stoch_k'] = stoch_k
    df['stoch_d'] = stoch_d
    
    # Williams %R
    df['williams_r'] = calculate_williams_r(df)
    
    # ATR
    df['atr'] = calculate_atr(df)
    df['atr_ratio'] = df['atr'] / df['close']  # Normalized ATR
    
    # CCI
    df['cci'] = calculate_cci(df)
    
    # Momentum and Rate of Change
    df['momentum'] = calculate_momentum(df)
    df['roc'] = calculate_rate_of_change(df)
    
    # Volume indicators
    df['volume_sma'] = calculate_volume_sma(df)
    df['volume_ratio'] = df['volume'] / df['volume_sma']
    df['obv'] = calculate_obv(df)
    df['pvt'] = calculate_price_volume_trend(df)
    
    # Price-based features
    df['price_change'] = df['close'].pct_change()
    df['high_low_ratio'] = df['high'] / df['low']
    df['close_open_ratio'] = df['close'] / df['open']
    
    # Moving average crossovers
    df['sma_cross'] = (df['sma_fast'] > df['sma_slow']).astype(int)
    df['ema_cross'] = (df['ema_12'] > df['ema_26']).astype(int)
    
    # --- Create Target Variable ---
    # 1 if the next period's close is higher than the current, 0 otherwise
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
    
    # Drop rows with NaN values created by indicators/shifting
    df.dropna(inplace=True)
    
    return df

def train_model(data):
    """
    Trains a simple Logistic Regression model.
    """
    logger.info("Starting ML model training...")
    
    # 1. Create Features and Labels
    df = create_features(data)
    
    if df.empty:
        logger.warning("Not enough data to create features for model training.")
        return None

    # Select features for the model
    feature_cols = [
        'rsi', 'macd', 'macd_signal', 'sma_fast', 'sma_slow',
        'ema_12', 'ema_26', 'bb_width', 'bb_position', 'stoch_k', 'stoch_d',
        'williams_r', 'atr_ratio', 'cci', 'momentum', 'roc', 'volume_ratio',
        'obv', 'pvt', 'price_change', 'high_low_ratio', 'close_open_ratio',
        'sma_cross', 'ema_cross'
    ]
    
    # Filter out any features that might have NaN values
    available_features = [col for col in feature_cols if col in df.columns and not df[col].isna().any()]
    
    if len(available_features) < 10:  # Need minimum features
        logger.warning(f"Only {len(available_features)} features available, using basic features")
        available_features = ['rsi', 'macd', 'macd_signal', 'sma_fast', 'sma_slow']
    
    X = df[available_features]
    y = df['target']

    if len(X) < 20: # Need a minimum amount of data to train
        logger.warning("Not enough data points to train the model after feature creation.")
        return None

    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    # 3. Scale features for better model performance
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 4. Train multiple models and select the best
    models = {
        'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    }
    
    best_model = None
    best_score = 0
    
    for name, model in models.items():
        try:
            model.fit(X_train_scaled, y_train)
            score = model.score(X_test_scaled, y_test)
            logger.info(f"{name} accuracy: {score:.4f}")
            
            if score > best_score:
                best_score = score
                best_model = model
                
        except Exception as e:
            logger.warning(f"Failed to train {name}: {e}")
    
    if best_model is None:
        logger.error("All models failed to train")
        return None
    
    # 5. Evaluate best model
    logger.info(f"Best model accuracy: {best_score:.4f}")
    
    # Store scaler with the model for later use
    best_model.scaler = scaler
    best_model.feature_names = available_features
    
    return best_model
