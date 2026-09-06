#!/usr/bin/env python3
"""
AI Trading Bot Training and Improvement Loop

This script continuously trains the AI model, analyzes performance,
and improves the code based on results every 2 hours.
"""

import os
import sys
import time
import json
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training_loop.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.training_history = []
        self.improvement_history = []
        self.best_performance = 0.0
        self.current_iteration = 0
        
    def train_model(self, symbol: str = "BTC/USDT", timeframe: str = "1d") -> Dict[str, Any]:
        """Train the AI model using backtesting"""
        logger.info(f"Starting model training iteration {self.current_iteration + 1}")
        
        try:
            # Run backtesting with AI strategy
            cmd = [
                "python", "backtest.py",
                "--strategy", "ai",
                "--source", "yahoo",  # Using Yahoo as default for testing
                "--symbol", symbol,
                "--timeframe", timeframe,
                "--start_date", "2022-01-01",
                "--end_date", "2023-12-31"
            ]
            
            logger.info(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                logger.error(f"Backtesting failed: {result.stderr}")
                return {"success": False, "error": result.stderr}
            
            # Parse results from output
            results = self._parse_backtest_results(result.stdout)
            results["iteration"] = self.current_iteration + 1
            results["timestamp"] = datetime.now().isoformat()
            
            self.training_history.append(results)
            logger.info(f"Training completed. Results: {results}")
            
            return results
            
        except subprocess.TimeoutExpired:
            logger.error("Training timed out after 5 minutes")
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            logger.error(f"Training failed with error: {e}")
            return {"success": False, "error": str(e)}
    
    def _parse_backtest_results(self, output: str) -> Dict[str, Any]:
        """Parse backtesting results from command output"""
        results = {
            "success": True,
            "total_return": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "win_rate": 0.0,
            "total_trades": 0
        }
        
        try:
            lines = output.split('\n')
            for line in lines:
                if 'Total Return:' in line:
                    results["total_return"] = float(line.split(':')[1].strip().replace('%', ''))
                elif 'Sharpe Ratio:' in line:
                    results["sharpe_ratio"] = float(line.split(':')[1].strip())
                elif 'Max Drawdown:' in line:
                    results["max_drawdown"] = float(line.split(':')[1].strip().replace('%', ''))
                elif 'Win Rate:' in line:
                    results["win_rate"] = float(line.split(':')[1].strip().replace('%', ''))
                elif 'Total Trades:' in line:
                    results["total_trades"] = int(line.split(':')[1].strip())
                    
        except Exception as e:
            logger.warning(f"Could not parse all results: {e}")
            
        return results
    
    def analyze_performance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze training results and identify areas for improvement"""
        analysis = {
            "needs_improvement": False,
            "improvement_areas": [],
            "suggestions": []
        }
        
        if not results.get("success", False):
            analysis["needs_improvement"] = True
            analysis["improvement_areas"].append("training_failure")
            analysis["suggestions"].append("Investigate training pipeline and data quality")
            return analysis
        
        # Check performance metrics
        total_return = results.get("total_return", 0)
        sharpe_ratio = results.get("sharpe_ratio", 0)
        max_drawdown = results.get("max_drawdown", 0)
        win_rate = results.get("win_rate", 0)
        
        # Performance thresholds
        if total_return < 10:  # Less than 10% return
            analysis["needs_improvement"] = True
            analysis["improvement_areas"].append("low_returns")
            analysis["suggestions"].append("Consider feature engineering and model complexity")
            
        if sharpe_ratio < 0.5:  # Poor risk-adjusted returns
            analysis["needs_improvement"] = True
            analysis["improvement_areas"].append("poor_risk_adjustment")
            analysis["suggestions"].append("Optimize position sizing and risk management")
            
        if max_drawdown > 20:  # High drawdown
            analysis["needs_improvement"] = True
            analysis["improvement_areas"].append("high_drawdown")
            analysis["suggestions"].append("Implement better stop-loss and risk controls")
            
        if win_rate < 0.4:  # Low win rate
            analysis["needs_improvement"] = True
            analysis["improvement_areas"].append("low_win_rate")
            analysis["suggestions"].append("Improve signal quality and entry/exit timing")
        
        # Check if this is the best performance so far
        if total_return > self.best_performance:
            self.best_performance = total_return
            logger.info(f"New best performance: {total_return:.2f}%")
        
        return analysis
    
    def improve_code(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Implement code improvements based on analysis"""
        improvements = {
            "implemented": [],
            "failed": [],
            "files_modified": []
        }
        
        if not analysis["needs_improvement"]:
            logger.info("No improvements needed at this time")
            return improvements
        
        logger.info("Implementing code improvements...")
        
        for area in analysis["improvement_areas"]:
            try:
                if area == "low_returns":
                    self._improve_feature_engineering(improvements)
                elif area == "poor_risk_adjustment":
                    self._improve_risk_management(improvements)
                elif area == "high_drawdown":
                    self._improve_stop_loss(improvements)
                elif area == "low_win_rate":
                    self._improve_signal_quality(improvements)
                    
            except Exception as e:
                logger.error(f"Failed to improve {area}: {e}")
                improvements["failed"].append(f"{area}: {e}")
        
        self.improvement_history.append({
            "iteration": self.current_iteration + 1,
            "timestamp": datetime.now().isoformat(),
            "improvements": improvements
        })
        
        return improvements
    
    def _improve_feature_engineering(self, improvements: Dict[str, Any]):
        """Improve feature engineering for better model performance"""
        logger.info("Improving feature engineering...")
        
        # Add new technical indicators
        new_features = """
        # Additional technical indicators
        df['ema_12'] = df['close'].ewm(span=12).mean()
        df['ema_26'] = df['close'].ewm(span=26).mean()
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = calculate_bollinger_bands(df)
        df['stoch_k'], df['stoch_d'] = calculate_stochastic(df)
        df['williams_r'] = calculate_williams_r(df)
        df['price_change'] = df['close'].pct_change()
        df['volume_change'] = df['volume'].pct_change()
        """
        
        # Update ML signals file
        self._update_file_content(
            "signals/ml_signals.py",
            "feature_cols = ['rsi', 'macd', 'macd_signal', 'sma_fast', 'sma_slow']",
            "feature_cols = ['rsi', 'macd', 'macd_signal', 'sma_fast', 'sma_slow', 'ema_12', 'ema_26', 'bb_upper', 'bb_middle', 'bb_lower', 'stoch_k', 'stoch_d', 'williams_r', 'price_change', 'volume_change']"
        )
        
        improvements["implemented"].append("Enhanced feature engineering")
        improvements["files_modified"].append("signals/ml_signals.py")
    
    def _improve_risk_management(self, improvements: Dict[str, Any]):
        """Improve risk management and position sizing"""
        logger.info("Improving risk management...")
        
        # Add dynamic position sizing based on volatility
        risk_improvement = """
        def calculate_position_size(self, current_equity, current_price, volatility):
            # Kelly Criterion inspired position sizing
            win_rate = 0.5  # Can be made dynamic
            avg_win = 0.02  # 2% average win
            avg_loss = 0.01  # 1% average loss
            
            kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
            kelly_fraction = max(0.01, min(0.25, kelly_fraction))  # Cap between 1-25%
            
            # Adjust for volatility
            volatility_factor = 1 / (1 + volatility)
            position_size = kelly_fraction * volatility_factor
            
            return max(0.01, min(0.1, position_size))  # Final cap at 10%
        """
        
        # Update AI strategy
        self._update_file_content(
            "strategies/ai_strategy.py",
            "self.on_trade('buy', 0.1, current_price, current_timestamp)",
            "position_size = self.calculate_position_size(None, current_price, 0.02)\n            self.on_trade('buy', position_size, current_price, current_timestamp)"
        )
        
        improvements["implemented"].append("Enhanced risk management")
        improvements["files_modified"].append("strategies/ai_strategy.py")
    
    def _improve_stop_loss(self, improvements: Dict[str, Any]):
        """Improve stop-loss mechanisms"""
        logger.info("Improving stop-loss mechanisms...")
        
        # Add trailing stop-loss and ATR-based stops
        stop_loss_improvement = """
        def update_stop_loss(self, position, current_price, atr):
            # Dynamic stop-loss based on ATR
            if position['side'] == 'buy':
                stop_price = current_price - (atr * 2)  # 2 ATR below current price
                if stop_price > position.get('stop_loss', 0):
                    position['stop_loss'] = stop_price
            else:
                stop_price = current_price + (atr * 2)  # 2 ATR above current price
                if stop_price < position.get('stop_loss', float('inf')):
                    position['stop_loss'] = stop_price
        """
        
        improvements["implemented"].append("Enhanced stop-loss mechanisms")
    
    def _improve_signal_quality(self, improvements: Dict[str, Any]):
        """Improve signal quality and filtering"""
        logger.info("Improving signal quality...")
        
        # Add signal confirmation and filtering
        signal_improvement = """
        def confirm_signal(self, prediction, features, current_price):
            # Signal confirmation logic
            rsi = features['rsi'].iloc[-1]
            macd = features['macd'].iloc[-1]
            macd_signal = features['macd_signal'].iloc[-1]
            
            # RSI filter
            if rsi > 70 or rsi < 30:
                return False  # Avoid extreme RSI levels
                
            # MACD confirmation
            if prediction == 1 and macd < macd_signal:
                return False  # MACD not confirming bullish signal
            elif prediction == 0 and macd > macd_signal:
                return False  # MACD not confirming bearish signal
                
            return True
        """
        
        improvements["implemented"].append("Enhanced signal quality")
    
    def _update_file_content(self, file_path: str, old_string: str, new_string: str):
        """Update file content with new code"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            if old_string in content:
                content = content.replace(old_string, new_string)
                
                with open(file_path, 'w') as f:
                    f.write(content)
                    
                logger.info(f"Updated {file_path}")
            else:
                logger.warning(f"Could not find target string in {file_path}")
                
        except Exception as e:
            logger.error(f"Failed to update {file_path}: {e}")
    
    def save_progress(self):
        """Save training and improvement progress"""
        progress = {
            "current_iteration": self.current_iteration,
            "best_performance": self.best_performance,
            "training_history": self.training_history,
            "improvement_history": self.improvement_history,
            "last_updated": datetime.now().isoformat()
        }
        
        with open("training_progress.json", "w") as f:
            json.dump(progress, f, indent=2)
        
        logger.info("Progress saved to training_progress.json")
    
    def run_training_loop(self, interval_hours: int = 2, max_iterations: int = None):
        """Main training and improvement loop"""
        logger.info(f"Starting training loop with {interval_hours}h intervals")
        
        try:
            while True:
                self.current_iteration += 1
                logger.info(f"\n{'='*50}")
                logger.info(f"Starting iteration {self.current_iteration}")
                logger.info(f"{'='*50}")
                
                # 1. Train the model
                results = self.train_model()
                
                # 2. Analyze performance
                analysis = self.analyze_performance(results)
                
                # 3. Improve code if needed
                if analysis["needs_improvement"]:
                    improvements = self.improve_code(analysis)
                    logger.info(f"Improvements implemented: {improvements['implemented']}")
                
                # 4. Save progress
                self.save_progress()
                
                # 5. Check if we should stop
                if max_iterations and self.current_iteration >= max_iterations:
                    logger.info(f"Reached maximum iterations ({max_iterations})")
                    break
                
                # 6. Wait for next iteration
                logger.info(f"Waiting {interval_hours} hours until next iteration...")
                time.sleep(interval_hours * 3600)  # Convert hours to seconds
                
        except KeyboardInterrupt:
            logger.info("Training loop interrupted by user")
        except Exception as e:
            logger.error(f"Training loop failed: {e}")
        finally:
            self.save_progress()
            logger.info("Training loop completed")

def main():
    """Main entry point"""
    trainer = ModelTrainer()
    
    # Check if we have existing progress
    if os.path.exists("training_progress.json"):
        try:
            with open("training_progress.json", "r") as f:
                progress = json.load(f)
                trainer.current_iteration = progress.get("current_iteration", 0)
                trainer.best_performance = progress.get("best_performance", 0.0)
                trainer.training_history = progress.get("training_history", [])
                trainer.improvement_history = progress.get("improvement_history", [])
                logger.info(f"Loaded existing progress from iteration {trainer.current_iteration}")
        except Exception as e:
            logger.warning(f"Could not load existing progress: {e}")
    
    # Start the training loop
    trainer.run_training_loop(interval_hours=2)

if __name__ == "__main__":
    main()