import pandas as pd
import numpy as np

def calculate_performance_metrics(portfolio, data):
    """
    Calculates and returns a dictionary of performance metrics.
    
    :param portfolio: The portfolio object after the backtest.
    :param data: The historical price data (DataFrame) used for the backtest.
    """
    if not portfolio.trades:
        return {
            "Total Return (%)": 0,
            "Sharpe Ratio": 0,
            "Max Drawdown (%)": 0,
            "Win Rate (%)": 0,
            "Total Trades": 0,
        }

    trades_df = pd.DataFrame(portfolio.trades)
    
    # --- Calculate Total Return ---
        # --- Calculate Total Return ---
    # --- Calculate Total Return ---
    final_value = portfolio.get_total_equity({trades_df['symbol'].iloc[-1]: trades_df['price'].iloc[-1]})
    total_return = ((final_value - portfolio.initial_cash) / portfolio.initial_cash) * 100

    total_return = ((final_value - portfolio.initial_cash) / portfolio.initial_cash) * 100

    # --- Calculate PnL per trade ---
    # This is a simplified PnL calculation
    pnl = []
    for i in range(len(trades_df)):
        if trades_df['side'].iloc[i] == 'sell':
            # Find the corresponding buy
            buy_trades = trades_df[(trades_df['side'] == 'buy') & (trades_df.index < i)]
            if not buy_trades.empty:
                # Simple FIFO logic
                buy_price = buy_trades['price'].iloc[-1]
                pnl.append((trades_df['price'].iloc[i] - buy_price) * trades_df['quantity'].iloc[i])

    # --- Win Rate ---
    wins = [p for p in pnl if p > 0]
    win_rate = (len(wins) / len(pnl)) * 100 if pnl else 0

    # --- Sharpe Ratio (simplified) ---
    if len(pnl) < 2:
        sharpe_ratio = 0
    else:
        daily_returns = pd.Series(pnl).pct_change().dropna()
        if daily_returns.std() == 0 or len(daily_returns) < 2:
            sharpe_ratio = 0
        else:
            sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252) # Annualized

    # --- Max Drawdown (simplified) ---
    # Create a series of portfolio values over time
    portfolio_values = []
    temp_cash = portfolio.initial_cash
    for _, trade in trades_df.iterrows():
        if trade['side'] == 'buy':
            temp_cash -= trade['cost']
        else:
            temp_cash += trade['cost']
        portfolio_values.append(temp_cash)
    
    values_series = pd.Series(portfolio_values)
    peak = values_series.expanding(min_periods=1).max()
    drawdown = (values_series - peak) / peak
    max_drawdown = drawdown.min() * 100

    return {
        "Total Return (%)": round(total_return, 2),
        "Sharpe Ratio": round(sharpe_ratio, 2),
        "Max Drawdown (%)": round(max_drawdown, 2),
        "Win Rate (%)": round(win_rate, 2),
        "Total Trades": len(trades_df),
    }
