import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from signals.rsi import calculate_rsi
from signals.macd import calculate_macd
from signals.moving_average import calculate_moving_average
from utils.logger import setup_logger

logger = setup_logger()

def create_features(data):
    """
    Creates features from the historical data for the ML model.
    """
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # --- Add Technical Indicators as Features ---
    df['rsi'] = calculate_rsi(df)
    df['macd'], df['macd_signal'] = calculate_macd(df)
    df['sma_fast'] = calculate_moving_average(df, period=20)
    df['sma_slow'] = calculate_moving_average(df, period=50)
    
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

    feature_cols = ['rsi', 'macd', 'macd_signal', 'sma_fast', 'sma_slow']
    X = df[feature_cols]
    y = df['target']

    if len(X) < 20: # Need a minimum amount of data to train
        logger.warning("Not enough data points to train the model after feature creation.")
        return None

    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    # 3. Train Model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # 4. Evaluate (for logging purposes)
    accuracy = model.score(X_test, y_test)
    logger.info(f"Model trained. Test Accuracy: {accuracy:.2f}")
    
    return model
