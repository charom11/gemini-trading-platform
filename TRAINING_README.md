# AI Trading Bot Training and Improvement System

This system continuously trains AI models for cryptocurrency trading, analyzes performance, and automatically improves the code based on results every 2 hours.

## 🚀 Features

- **Continuous Training**: Automatically retrains AI models every 2 hours
- **Performance Analysis**: Analyzes trading results and identifies improvement areas
- **Automatic Code Improvement**: Implements enhancements based on performance analysis
- **Enhanced Feature Engineering**: 25+ technical indicators for better model performance
- **Risk Management**: Dynamic position sizing and stop-loss mechanisms
- **Progress Tracking**: Saves training progress and can resume from interruptions
- **Multiple ML Models**: Tests Logistic Regression and Random Forest, selects the best

## 📁 Project Structure

```
├── train_and_improve.py      # Main training and improvement loop
├── start_training.py         # Script to start the training loop
├── config/
│   └── training_config.py    # Configuration parameters
├── signals/
│   ├── ml_signals.py         # Enhanced ML signal generation
│   └── technical_indicators.py # Additional technical indicators
├── strategies/
│   └── ai_strategy.py        # Enhanced AI trading strategy
└── requirements_training.txt  # Training-specific dependencies
```

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements_training.txt
   ```

2. **Verify Installation**:
   ```bash
   python -c "import sklearn, pandas, numpy; print('Dependencies installed successfully')"
   ```

## 🚀 Quick Start

### Start Training Loop
```bash
python start_training.py
```

The system will:
1. Train the AI model using historical data
2. Analyze performance metrics
3. Implement code improvements if needed
4. Wait 2 hours and repeat

### Manual Training (Single Run)
```bash
python train_and_improve.py
```

## 📊 What Gets Improved

### 1. Feature Engineering
- **Basic Indicators**: RSI, MACD, Moving Averages
- **Advanced Indicators**: Bollinger Bands, Stochastic, Williams %R, ATR, CCI
- **Volume Indicators**: OBV, PVT, Volume ratios
- **Price Features**: Price changes, ratios, crossovers

### 2. Risk Management
- **Dynamic Position Sizing**: Kelly Criterion with volatility adjustment
- **Stop-Loss Mechanisms**: ATR-based trailing stops
- **Signal Confirmation**: RSI and MACD filters

### 3. Model Selection
- **Multiple Algorithms**: Tests Logistic Regression and Random Forest
- **Feature Scaling**: StandardScaler for better performance
- **Hyperparameter Optimization**: Configurable model parameters

## ⚙️ Configuration

Edit `config/training_config.py` to customize:

```python
# Training intervals
LOOP_CONFIG = {
    "interval_hours": 2,        # Change training frequency
    "max_iterations": None,     # Set max iterations or None for infinite
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "min_total_return": 10.0,   # Minimum 10% return
    "min_sharpe_ratio": 0.5,    # Minimum Sharpe ratio
    "max_drawdown": 20.0,       # Maximum 20% drawdown
}
```

## 📈 Performance Metrics

The system tracks and analyzes:

- **Total Return**: Overall portfolio performance
- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Model Accuracy**: ML model prediction accuracy

## 🔄 Improvement Triggers

### Low Returns (< 10%)
- Enhances feature engineering
- Tries different ML models
- Optimizes hyperparameters

### Poor Risk Adjustment (Sharpe < 0.5)
- Improves risk management
- Optimizes position sizing
- Adds stop-loss mechanisms

### High Drawdown (> 20%)
- Implements stop-loss
- Adds risk controls
- Optimizes entry timing

### Low Win Rate (< 40%)
- Improves signal quality
- Adds confirmation filters
- Optimizes entry/exit logic

## 📝 Logging and Monitoring

- **Training Logs**: `training_loop.log`
- **Progress Tracking**: `training_progress.json`
- **Model Backups**: `models/backup/`

## 🛑 Stopping the Training Loop

### Graceful Shutdown
```bash
# Press Ctrl+C in the terminal
# The system will save progress and exit cleanly
```

### Force Stop
```bash
# Find the process ID
ps aux | grep train_and_improve

# Kill the process
kill -9 <PID>
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements_training.txt
   ```

2. **Data Source Issues**: Check internet connection and API keys
   ```bash
   # Test data source
   python -c "from data.yahoo_finance import YahooFinanceData; print('Data source OK')"
   ```

3. **Memory Issues**: Reduce feature set or data size in config

4. **Training Timeouts**: Increase timeout in `train_and_improve.py`

### Performance Optimization

- **Reduce Features**: Edit `FEATURE_CONFIG` in training config
- **Shorter Timeframes**: Use smaller date ranges for faster training
- **Model Selection**: Limit to fewer ML models

## 📚 Advanced Usage

### Custom Improvement Logic
Edit `train_and_improve.py` to add custom improvement strategies:

```python
def _custom_improvement(self, improvements):
    """Custom improvement logic"""
    # Your custom code here
    pass
```

### Custom Features
Add new technical indicators in `signals/technical_indicators.py`:

```python
def calculate_custom_indicator(df):
    """Your custom indicator"""
    return df['close'].rolling(20).mean()
```

### Model Persistence
The system automatically saves models. To load a specific model:

```python
import joblib
model = joblib.load('models/backup/model_iteration_5.pkl')
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This is for educational and research purposes. Trading cryptocurrencies involves substantial risk. Always test thoroughly in paper trading mode before using real funds.

## 🆘 Support

For issues and questions:
1. Check the logs in `training_loop.log`
2. Review the troubleshooting section
3. Open an issue on GitHub
4. Check the documentation

---

**Happy Trading and Learning! 🚀📈**