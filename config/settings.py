# API Keys
BINANCE_API_KEY = "4iqCjotOZYo92gyNCAkWHUNwbhY8gDSTkwZPaeEHNju8pNrT8aXmp4DbpcrJZLFR"
BINANCE_API_SECRET = "g2jItzPOPScHYzakzJGZShMtbTpYo5emLUagK5eR2034gFyV9d92VMFT2rHsnI8S"

BYBIT_API_KEY = "YOUR_API_KEY"
BYBIT_API_SECRET = "YOUR_API_SECRET"

COINBASE_PRO_API_KEY = "YOUR_API_KEY"
COINBASE_PRO_API_SECRET = "YOUR_API_SECRET"
COINBASE_PRO_PASSWORD = "YOUR_PASSWORD"

# Alpaca API Keys
ALPACA_API_KEY = "PKDTWPY9LSF7SP7M38GJ"
ALPACA_API_SECRET = "7P1fWaKLp6wD5l1hgG0JkK85L0gPY694dqFq3NEE"
ALPACA_PAPER = True # Set to False for live trading

# Strategy Configurations
GRID_CONFIG = {
    "levels": 10,
    "quantity": 0.01,
}

MEAN_REVERSION_CONFIG = {
    "oversold_threshold": 30,
    "overbought_threshold": 70,
}

MOMENTUM_CONFIG = {
    "fast_period": 12,
    "slow_period": 26,
    "signal_period": 9,
    "stop_loss_pct": 0.05,  # 5%
    "take_profit_pct": 0.10, # 10%
}

MOMENTUM_ATR_CONFIG = {
    "fast_period": 12,
    "slow_period": 26,
    "signal_period": 9,
    "atr_period": 14,
    "atr_multiplier": 2.0,
}

MA_CROSSOVER_CONFIG = {
    "fast_period": 20,
    "slow_period": 50,
}
