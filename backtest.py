import argparse
from backtesting.engine import BacktestingEngine
from strategies.mean_reversion import MeanReversionStrategy
from strategies.momentum import MomentumStrategy
from strategies.grid import GridStrategy
from strategies.ma_crossover import MovingAverageCrossoverStrategy
from strategies.ai_strategy import AIStrategy
from strategies.momentum_atr import MomentumATRStrategy
from exchanges.binance import BinanceExchange
from data.yahoo_finance import YahooFinanceData
from exchanges.alpaca import AlpacaExchange
from config import settings
from utils.logger import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Gemini Backtesting Engine")
    parser.add_argument("--strategy", type=str, required=True, choices=["mean_reversion", "momentum", "grid", "ma_crossover", "ai", "momentum_atr"], help="Strategy to backtest")
    parser.add_argument("--source", type=str, default="binance", choices=["binance", "yahoo", "alpaca"], help="Data source to use")
    parser.add_argument("--symbol", type=str, required=True, help="Symbol to backtest (e.g., BTC/USDT or AAPL)")
    parser.add_argument("--timeframe", type=str, default="1d", help="Timeframe for data (e.g., 1d)")
    parser.add_argument("--start_date", type=str, default="2023-01-01", help="Start date for backtest (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, default="2023-12-31", help="End date for backtest (YYYY-MM-DD)")
    args = parser.parse_args()

    # --- Initialize Data Source ---
    datasource = None
    if args.source == "binance":
        datasource = BinanceExchange(api_key=settings.BINANCE_API_KEY, api_secret=settings.BINANCE_API_SECRET)
    elif args.source == "yahoo":
        datasource = YahooFinanceData()
    elif args.source == "alpaca":
        datasource = AlpacaExchange(
            api_key=settings.ALPACA_API_KEY, 
            api_secret=settings.ALPACA_API_SECRET, 
            paper=True
        )

    if not datasource:
        logger.error("Could not initialize data source.")
        return

    # --- Select Strategy ---
    strategy_map = {
        "mean_reversion": (MeanReversionStrategy, settings.MEAN_REVERSION_CONFIG),
        "momentum": (MomentumStrategy, settings.MOMENTUM_CONFIG),
        "grid": (GridStrategy, settings.GRID_CONFIG),
        "ma_crossover": (MovingAverageCrossoverStrategy, settings.MA_CROSSOVER_CONFIG),
        "ai": (AIStrategy, {}),
        "momentum_atr": (MomentumATRStrategy, settings.MOMENTUM_ATR_CONFIG),
    }
    
    if args.strategy not in strategy_map:
        logger.error("Invalid strategy specified.")
        return
        
    strategy_class, strategy_config = strategy_map[args.strategy]

    # --- Initialize and Run Backtesting Engine ---
    engine = BacktestingEngine(
        datasource=datasource,
        strategy_class=strategy_class,
        strategy_config=strategy_config,
        symbol=args.symbol,
        timeframe=args.timeframe,
        start_date=args.start_date,
        end_date=args.end_date
    )
    engine.run()

if __name__ == "__main__":
    main()