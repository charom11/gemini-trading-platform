#!/usr/bin/env python3
"""
Test Training System

This script tests the training system components without running the full loop.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from train_and_improve import ModelTrainer
from config.training_config import PERFORMANCE_THRESHOLDS, IMPROVEMENT_TRIGGERS
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_model_trainer():
    """Test the ModelTrainer class"""
    logger.info("Testing ModelTrainer class...")
    
    try:
        # Initialize trainer
        trainer = ModelTrainer()
        logger.info("✓ ModelTrainer initialized successfully")
        
        # Test performance analysis
        test_results = {
            "success": True,
            "total_return": 5.0,  # Below threshold
            "sharpe_ratio": 0.3,  # Below threshold
            "max_drawdown": 25.0, # Above threshold
            "win_rate": 0.35,     # Below threshold
            "total_trades": 50
        }
        
        analysis = trainer.analyze_performance(test_results)
        logger.info(f"✓ Performance analysis completed: {analysis}")
        
        # Test improvement logic
        if analysis["needs_improvement"]:
            improvements = trainer.improve_code(analysis)
            logger.info(f"✓ Code improvements: {improvements}")
        
        logger.info("✓ All tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    logger.info("Testing configuration...")
    
    try:
        logger.info(f"✓ Performance thresholds: {PERFORMANCE_THRESHOLDS}")
        logger.info(f"✓ Improvement triggers: {IMPROVEMENT_TRIGGERS}")
        logger.info("✓ Configuration loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"✗ Configuration test failed: {e}")
        return False

def test_feature_engineering():
    """Test feature engineering"""
    logger.info("Testing feature engineering...")
    
    try:
        from signals.technical_indicators import calculate_bollinger_bands, calculate_stochastic
        import pandas as pd
        import numpy as np
        
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        sample_data = pd.DataFrame({
            'open': np.random.randn(100).cumsum() + 100,
            'high': np.random.randn(100).cumsum() + 102,
            'low': np.random.randn(100).cumsum() + 98,
            'close': np.random.randn(100).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
        
        # Test indicators
        bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(sample_data)
        stoch_k, stoch_d = calculate_stochastic(sample_data)
        
        logger.info(f"✓ Bollinger Bands calculated: {len(bb_upper)} points")
        logger.info(f"✓ Stochastic calculated: {len(stoch_k)} points")
        logger.info("✓ Feature engineering test passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Feature engineering test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting training system tests...")
    logger.info("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Feature Engineering", test_feature_engineering),
        ("Model Trainer", test_model_trainer)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\nRunning {test_name} test...")
        if test_func():
            passed += 1
            logger.info(f"✓ {test_name} test PASSED")
        else:
            logger.error(f"✗ {test_name} test FAILED")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! The training system is ready to use.")
        logger.info("\nTo start the training loop, run:")
        logger.info("  python3 start_training.py")
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())