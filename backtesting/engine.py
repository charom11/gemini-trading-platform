import pandas as pd
from datetime import datetime, timezone
from .portfolio import Portfolio
from .performance import calculate_performance_metrics
from utils.logger import setup_logger

logger = setup_logger()

class BacktestingEngine:
    def __init__(self, datasource, strategy_class, strategy_config, symbol, timeframe, start_date, end_date):
        self.datasource = datasource
        self.strategy_class = strategy_class
        self.strategy_config = strategy_config
        self.symbol = symbol
        self.timeframe = timeframe
        self.start_date = start_date
        self.end_date = end_date
        self.portfolio = Portfolio()

    def run(self):
        logger.info(f"Starting backtest for {self.symbol} from {self.start_date} to {self.end_date}")

        # 1. Load Data
        logger.info("Loading historical data...")
        ohlcv = self.datasource.fetch_ohlcv(
            self.symbol, 
            timeframe=self.timeframe, 
            start_date=self.start_date, 
            end_date=self.end_date
        )

        if not ohlcv:
            logger.error("Could not fetch historical data for backtest.")
            return
        
        data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data.set_index('timestamp', inplace=True)
        
        # Filter data for the requested date range (as fetch might bring more)
        data = data[self.start_date:self.end_date]
        
        if data.empty:
            logger.error("No data available for the specified date range.")
            return

        logger.info(f"Loaded {len(data)} data points for backtesting.")

        # 2. Initialize Strategy
        strategy = self.strategy_class(
            symbol=self.symbol,
            config=self.strategy_config,
            on_trade=lambda side, qty, price, ts: self.portfolio.execute_trade(ts, self.symbol, side, qty, price)
        )

        # --- Special handling for AI Strategy: Train model first ---
        if hasattr(strategy, 'train'):
            logger.info("AI Strategy detected. Training model on full historical dataset...")
            strategy.train(ohlcv) # Pass the raw list of lists
            if strategy.model is None:
                logger.error("Model training failed. Aborting backtest.")
                return

        # 3. Main Backtesting Loop
        logger.info("Running strategy simulation...")
        for i in range(1, len(data)):
            historical_data_slice = data.iloc[0:i]
            current_candle = data.iloc[i-1]
            current_price = current_candle['close']
            current_timestamp = current_candle.name

            # --- Check for Trailing Stop-Loss ---
            if self.symbol in self.portfolio.positions:
                position = self.portfolio.positions[self.symbol]
                
                if 'trailing_stop_price' in position and current_price <= position['trailing_stop_price']:
                    logger.info(f"[{current_timestamp}] TRAILING STOP triggered at {current_price:.2f}")
                    self.portfolio.execute_trade(current_timestamp, self.symbol, 'sell', position['quantity'], current_price)
                    continue # Skip to next candle
                
                # Update the trailing stop price if the current price is higher
                if 'atr' in self.strategy_config: # A bit of a hack to know if it's an ATR strategy
                    new_stop_price = current_price - (strategy.current_atr * self.strategy_config['atr_multiplier'])
                    if 'trailing_stop_price' not in position or new_stop_price > position['trailing_stop_price']:
                         position['trailing_stop_price'] = new_stop_price


            if len(historical_data_slice) > 50: # Ensure enough data for indicators
                # Pass current equity to the strategy for position sizing
                current_equity = self.portfolio.get_total_equity({self.symbol: current_price})
                strategy.execute(historical_data_slice, current_equity)

        # 4. Calculate and Display Results
        logger.info("Backtest finished. Calculating performance...")
        
        last_price = data['close'].iloc[-1]
        performance = calculate_performance_metrics(self.portfolio, data)

        print("\n--- Backtest Results ---")
        for key, value in performance.items():
            print(f"{key}: {value}")
        print("------------------------")
        
        final_value = self.portfolio.get_current_value({self.symbol: last_price})
        print(f"Initial Cash: ${self.portfolio.initial_cash:.2f}")
        print(f"Final Portfolio Value: ${final_value:.2f}")
        print("------------------------")

        # 5. Visualize Results
        from .visualizer import plot_backtest_results
        plot_backtest_results(self.portfolio, data, self.strategy_class.__name__, self.symbol)
