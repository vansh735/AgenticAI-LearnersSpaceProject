import yfinance as yf
import pandas as pd
from typing import Dict, Any

def calculate_rsi(data: pd.Series, window: int = 14) -> pd.Series:
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    avg_gain = gain.ewm(com=window - 1, min_periods=window).mean()
    avg_loss = loss.ewm(com=window - 1, min_periods=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_market_data(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="45d")
        
        if df.empty:
            return f"Error: No market data found for ticker {ticker}. It may be delisted or invalid."
        
        df['5_day_SMA'] = df['Close'].rolling(window=5).mean()
        df['20_day_SMA'] = df['Close'].rolling(window=20).mean()
        df['RSI_14'] = calculate_rsi(df['Close'], window=14)
        df['Daily_Return'] = df['Close'].pct_change()
        df['Volatility_20d'] = df['Daily_Return'].rolling(window=20).std() * (252 ** 0.5) # Annualized
        
        recent_df = df.tail(10).copy()
        
        output = []
        output.append(f"Market Data for {ticker} (Last 10 Trading Days):")
        output.append("-" * 50)
        
        for index, row in recent_df.iterrows():
            date_str = index.strftime('%Y-%m-%d')
            output.append(
                f"Date: {date_str} | Close: ${row['Close']:.2f} | "
                f"Volume: {int(row['Volume']):,} | "
                f"5d SMA: ${row['5_day_SMA']:.2f} | 20d SMA: ${row['20_day_SMA']:.2f} | "
                f"RSI: {row['RSI_14']:.2f} | Volatility: {row['Volatility_20d']:.2%}"
            )
            
        return "\n".join(output)

    except Exception as e:
        return f"Failed to retrieve or process market data for {ticker}. Exception: {str(e)}"
