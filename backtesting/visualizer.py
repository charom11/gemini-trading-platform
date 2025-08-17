import matplotlib.pyplot as plt
import pandas as pd
from .portfolio import Portfolio

def plot_backtest_results(portfolio: Portfolio, data: pd.DataFrame, strategy_name: str, symbol: str):
    """
    Generates and saves a plot of the backtest results.
    """
    trades_df = pd.DataFrame(portfolio.trades)
    if trades_df.empty:
        print("No trades to visualize.")
        return

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle(f'Backtest Results: {strategy_name} on {symbol}', fontsize=16)

    # --- Plot 1: Price and Trades ---
    ax1.plot(data.index, data['close'], label='Close Price', color='skyblue')
    
    # Plot Buy signals
    buy_trades = trades_df[trades_df['side'] == 'buy']
    ax1.plot(buy_trades['timestamp'], buy_trades['price'], '^', color='green', markersize=8, label='Buy Signal')
    
    # Plot Sell signals
    sell_trades = trades_df[trades_df['side'] == 'sell']
    ax1.plot(sell_trades['timestamp'], sell_trades['price'], 'v', color='red', markersize=8, label='Sell Signal')
    
    ax1.set_title('Price and Trades')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    # --- Plot 2: Equity Curve ---
    # Calculate portfolio value over time
    portfolio_values = []
    value_timestamps = []
    temp_portfolio = Portfolio(initial_cash=portfolio.initial_cash)
    
    trade_idx = 0
    for timestamp, row in data.iterrows():
        while trade_idx < len(trades_df) and pd.to_datetime(trades_df['timestamp'].iloc[trade_idx]) <= timestamp:
            trade = trades_df.iloc[trade_idx]
            temp_portfolio.execute_trade(trade['timestamp'], trade['symbol'], trade['side'], trade['quantity'], trade['price'])
            trade_idx += 1
        
        current_prices = {symbol: row['close']}
        portfolio_values.append(temp_portfolio.get_current_value(current_prices))
        value_timestamps.append(timestamp)

    ax2.plot(value_timestamps, portfolio_values, label='Portfolio Value', color='purple')
    ax2.set_title('Equity Curve')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Portfolio Value')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    # Save the figure
    filename = f"backtest_{symbol.replace('/', '_')}_{strategy_name}.png"
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(filename)
    plt.close()
    print(f"Backtest visualization saved to {filename}")
