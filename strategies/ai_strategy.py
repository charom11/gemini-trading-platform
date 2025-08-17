from utils.logger import setup_logger
from signals.ml_signals import train_model, create_features
import pandas as pd

logger = setup_logger()

class AIStrategy:
    def __init__(self, symbol, config, on_trade):
        self.symbol = symbol
        self.config = config
        self.on_trade = on_trade
        self.model = None
        self.last_signal = None

    def execute(self, data, current_equity=None):
        """
        Executes the AI-based strategy.
        """
        current_price = data['close'].iloc[-1]
        current_timestamp = data.index[-1]

        # --- The model should be trained by the backtesting engine before this is called ---
        if self.model is None:
            logger.error("AI model has not been trained. Please train the model before running the strategy.")
            return

        # --- Generate Signal for the latest data point ---
        # Create features for the most recent data
        latest_features_df = create_features(data.reset_index()[['timestamp', 'open', 'high', 'low', 'close', 'volume']].values.tolist())
        
        if latest_features_df.empty:
            return # Not enough data to generate features for the latest point

        latest_features = latest_features_df[['rsi', 'macd', 'macd_signal', 'sma_fast', 'sma_slow']].iloc[-1:]
        
        # Predict the signal (1 for up, 0 for down)
        prediction = self.model.predict(latest_features)[0]
        
        logger.debug(f"[{current_timestamp}] Price: {current_price:.2f}, AI Prediction: {'UP' if prediction == 1 else 'DOWN'}")

        # --- Trading Logic ---
        if prediction == 1 and self.last_signal != 'buy':
            logger.info(f"[{current_timestamp}] AI model predicts UP. Executing BUY.")
            self.on_trade('buy', 0.1, current_price, current_timestamp)
            self.last_signal = 'buy'
        elif prediction == 0 and self.last_signal != 'sell':
            logger.info(f"[{current_timestamp}] AI model predicts DOWN. Executing SELL.")
            self.on_trade('sell', 0.1, current_price, current_timestamp)
            self.last_signal = 'sell'

    def train(self, historical_data):
        """
        Trains the AI model on a full set of historical data.
        """
        self.model = train_model(historical_data)
