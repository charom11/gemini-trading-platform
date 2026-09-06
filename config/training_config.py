"""
Training Configuration for AI Trading Bot
"""

# Training Parameters
TRAINING_CONFIG = {
    "default_symbol": "BTC/USDT",
    "default_timeframe": "1d",
    "training_start_date": "2022-01-01",
    "training_end_date": "2023-12-31",
    "validation_split": 0.2,
    "random_state": 42,
    "min_data_points": 20,
    "feature_engineering": {
        "use_enhanced_features": True,
        "min_features": 10,
        "fallback_features": ['rsi', 'macd', 'macd_signal', 'sma_fast', 'sma_slow']
    }
}

# Model Configuration
MODEL_CONFIG = {
    "models": {
        "logistic_regression": {
            "class": "LogisticRegression",
            "params": {
                "random_state": 42,
                "max_iter": 1000,
                "C": 1.0
            }
        },
        "random_forest": {
            "class": "RandomForestClassifier",
            "params": {
                "n_estimators": 100,
                "random_state": 42,
                "max_depth": 10,
                "min_samples_split": 5,
                "min_samples_leaf": 2
            }
        }
    },
    "preprocessing": {
        "use_scaling": True,
        "scaler": "StandardScaler"
    }
}

# Performance Thresholds
PERFORMANCE_THRESHOLDS = {
    "min_total_return": 10.0,      # Minimum 10% return
    "min_sharpe_ratio": 0.5,       # Minimum Sharpe ratio
    "max_drawdown": 20.0,          # Maximum 20% drawdown
    "min_win_rate": 0.4,           # Minimum 40% win rate
    "min_accuracy": 0.55           # Minimum 55% model accuracy
}

# Improvement Triggers
IMPROVEMENT_TRIGGERS = {
    "low_returns": {
        "threshold": 10.0,
        "actions": ["enhance_features", "try_different_models", "optimize_hyperparameters"]
    },
    "poor_risk_adjustment": {
        "threshold": 0.5,
        "actions": ["improve_risk_management", "optimize_position_sizing", "add_stop_loss"]
    },
    "high_drawdown": {
        "threshold": 20.0,
        "actions": ["implement_stop_loss", "add_risk_controls", "optimize_entry_timing"]
    },
    "low_win_rate": {
        "threshold": 0.4,
        "actions": ["improve_signal_quality", "add_confirmation_filters", "optimize_entry_exit"]
    }
}

# Feature Engineering Configuration
FEATURE_CONFIG = {
    "technical_indicators": {
        "rsi": {"period": 14},
        "macd": {"fast": 12, "slow": 26, "signal": 9},
        "sma": {"fast": 20, "slow": 50},
        "ema": {"fast": 12, "slow": 26},
        "bollinger_bands": {"period": 20, "std_dev": 2.0},
        "stochastic": {"k_period": 14, "d_period": 3},
        "williams_r": {"period": 14},
        "atr": {"period": 14},
        "cci": {"period": 20},
        "momentum": {"period": 10},
        "roc": {"period": 10}
    },
    "volume_indicators": {
        "volume_sma": {"period": 20},
        "obv": {},
        "pvt": {}
    },
    "price_features": {
        "price_change": {},
        "high_low_ratio": {},
        "close_open_ratio": {}
    }
}

# Risk Management Configuration
RISK_CONFIG = {
    "position_sizing": {
        "max_position_size": 0.1,      # Maximum 10% of portfolio
        "min_position_size": 0.01,     # Minimum 1% of portfolio
        "kelly_cap": 0.25,             # Maximum Kelly fraction
        "volatility_adjustment": True
    },
    "stop_loss": {
        "use_trailing_stop": True,
        "atr_multiplier": 2.0,         # 2 ATR for stop loss
        "max_loss_per_trade": 0.02     # Maximum 2% loss per trade
    },
    "signal_confirmation": {
        "use_rsi_filter": True,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "use_macd_confirmation": True
    }
}

# Training Loop Configuration
LOOP_CONFIG = {
    "interval_hours": 2,
    "max_iterations": None,            # None for infinite loop
    "save_progress": True,
    "progress_file": "training_progress.json",
    "log_file": "training_loop.log",
    "backup_models": True,
    "model_backup_dir": "models/backup/"
}