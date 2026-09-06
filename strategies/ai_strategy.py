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

        # Get the features that the model was trained on
        model_features = getattr(self.model, 'feature_names', ['rsi', 'macd', 'macd_signal', 'sma_fast', 'sma_slow'])
        available_features = [col for col in model_features if col in latest_features_df.columns]
        
        if len(available_features) < len(model_features):
            logger.warning(f"Missing features: {set(model_features) - set(available_features)}")
        
        latest_features = latest_features_df[available_features].iloc[-1:]
        
        # Scale features if scaler is available
        if hasattr(self.model, 'scaler'):
            latest_features_scaled = self.model.scaler.transform(latest_features)
            prediction = self.model.predict(latest_features_scaled)[0]
        else:
            prediction = self.model.predict(latest_features)[0]
        
        logger.debug(f"[{current_timestamp}] Price: {current_price:.2f}, AI Prediction: {'UP' if prediction == 1 else 'DOWN'}")

        # --- Trading Logic with Enhanced Risk Management ---
        if prediction == 1 and self.last_signal != 'buy':
            # Confirm signal and calculate position size
            if self.confirm_signal(prediction, latest_features_df, current_price):
                position_size = self.calculate_position_size(None, current_price, 0.02)
                logger.info(f"[{current_timestamp}] AI model predicts UP. Executing BUY with {position_size:.3f} position size.")
                self.on_trade('buy', position_size, current_price, current_timestamp)
                self.last_signal = 'buy'
            else:
                logger.info(f"[{current_timestamp}] AI model predicts UP but signal not confirmed. Skipping trade.")
        elif prediction == 0 and self.last_signal != 'sell':
            # Confirm signal and calculate position size
            if self.confirm_signal(prediction, latest_features_df, current_price):
                position_size = self.calculate_position_size(None, current_price, 0.02)
                logger.info(f"[{current_timestamp}] AI model predicts DOWN. Executing SELL with {position_size:.3f} position size.")
                self.on_trade('sell', position_size, current_price, current_timestamp)
                self.last_signal = 'sell'
            else:
                logger.info(f"[{current_timestamp}] AI model predicts DOWN but signal not confirmed. Skipping trade.")

    def calculate_position_size(self, current_equity, current_price, volatility=0.02):
        """
        Calculate position size using Kelly Criterion and volatility adjustment.
        """
        # Kelly Criterion inspired position sizing
        win_rate = 0.5  # Can be made dynamic based on historical performance
        avg_win = 0.02  # 2% average win
        avg_loss = 0.01  # 1% average loss
        
        kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
        kelly_fraction = max(0.01, min(0.25, kelly_fraction))  # Cap between 1-25%
        
        # Adjust for volatility
        volatility_factor = 1 / (1 + volatility)
        position_size = kelly_fraction * volatility_factor
        
        return max(0.01, min(0.1, position_size))  # Final cap at 10%
    
    def confirm_signal(self, prediction, features, current_price):
        """
        Confirm trading signal using additional filters.
        """
        try:
            rsi = features.get('rsi', 50).iloc[-1] if hasattr(features, 'iloc') else features.get('rsi', 50)
            macd = features.get('macd', 0).iloc[-1] if hasattr(features, 'iloc') else features.get('macd', 0)
            macd_signal = features.get('macd_signal', 0).iloc[-1] if hasattr(features, 'iloc') else features.get('macd_signal', 0)
            
            # RSI filter - avoid extreme levels
            if rsi > 70 or rsi < 30:
                return False
                
            # MACD confirmation
            if prediction == 1 and macd < macd_signal:
                return False  # MACD not confirming bullish signal
            elif prediction == 0 and macd > macd_signal:
                return False  # MACD not confirming bearish signal
                
            return True
            
        except Exception as e:
            logger.warning(f"Signal confirmation failed: {e}")
            return True  # Default to allowing the signal
    
    def train(self, historical_data):
        """
        Trains the AI model on a full set of historical data.
        """
        self.model = train_model(historical_data)
