import argparse
from core.engine import TradingEngine
from exchanges.binance import BinanceExchange
from strategies.grid import GridStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.momentum import MomentumStrategy
from config import settings
from utils.logger import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Gemini Trading Bot")
    parser.add_argument("--strategy", type=str, required=True, choices=["grid", "mean_reversion", "momentum"], help="Trading strategy to use")
    parser.add_argument("--mode", type=str, required=True, choices=["paper", "live"], help="Trading mode")
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTC/USDT)")
    parser.add_argument("--exchange", type=str, default="binance", choices=["binance"], help="Exchange to use")
    args = parser.parse_args()

    logger.info(f"Starting trading bot on {args.exchange} with strategy: {args.strategy}, mode: {args.mode}, symbol: {args.symbol}")

    # --- Initialize Exchange ---
    exchange = None
    if args.exchange == "binance":
        real_exchange = BinanceExchange(api_key=settings.BINANCE_API_KEY, api_secret=settings.BINANCE_API_SECRET)
        if args.mode == "paper":
            from exchanges.paper_trading import PaperTradingExchange
            exchange = PaperTradingExchange(real_exchange)
        else:
            exchange = real_exchange
    
    if not exchange:
        logger.error("Could not initialize exchange.")
        return

    # --- Initialize Strategy ---
    strategy = None
    if args.strategy == "grid":
        strategy = GridStrategy(symbol=args.symbol, exchange=exchange, config=settings.GRID_CONFIG)
    elif args.strategy == "mean_reversion":
        from signals.rsi import calculate_rsi
        strategy = MeanReversionStrategy(
            symbol=args.symbol, 
            exchange=exchange,
            signal_generator=calculate_rsi,
            config=settings.MEAN_REVERSION_CONFIG
        )
    elif args.strategy == "momentum":
        from signals.macd import calculate_macd
        strategy = MomentumStrategy(
            symbol=args.symbol,
            exchange=exchange,
            signal_generator=calculate_macd,
            config=settings.MOMENTUM_CONFIG
        )
    
    if not strategy:
        logger.error("Invalid strategy specified.")
        return

    # --- Initialize and Run Trading Engine ---
    engine = TradingEngine(
        strategy=strategy,
        exchange=exchange,
        mode=args.mode,
        symbol=args.symbol
    )
    engine.run()

if __name__ == "__main__":
    main()
