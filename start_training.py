#!/usr/bin/env python3
"""
Start Training Loop Script

This script starts the AI trading bot training and improvement loop.
Run this to begin continuous training and improvement.
"""

import sys
import os
import signal
import time
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from train_and_improve import ModelTrainer
from config.training_config import LOOP_CONFIG
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOOP_CONFIG['log_file']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    logger.info(f"Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)

def main():
    """Main entry point"""
    logger.info("Starting AI Trading Bot Training Loop")
    logger.info("=" * 50)
    
    # Create necessary directories
    Path("models/backup").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Initialize trainer
        trainer = ModelTrainer()
        
        # Check for existing progress
        if os.path.exists(LOOP_CONFIG['progress_file']):
            logger.info("Found existing training progress, resuming...")
        
        # Start training loop
        logger.info(f"Training loop will run every {LOOP_CONFIG['interval_hours']} hours")
        logger.info("Press Ctrl+C to stop the training loop")
        
        trainer.run_training_loop(
            interval_hours=LOOP_CONFIG['interval_hours'],
            max_iterations=LOOP_CONFIG['max_iterations']
        )
        
    except KeyboardInterrupt:
        logger.info("Training loop interrupted by user")
    except Exception as e:
        logger.error(f"Training loop failed with error: {e}")
        raise
    finally:
        logger.info("Training loop completed")

if __name__ == "__main__":
    main()