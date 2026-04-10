import pandas as pd
import numpy as np


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw stock data - handle nulls, types, duplicates."""
    df = df.copy()

    # Standardize column names
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    # Drop duplicates
    df.drop_duplicates(subset=["date", "ticker"], inplace=True)

    # Drop rows with missing OHLCV
    df.dropna(subset=["open", "high", "low", "close", "volume"], inplace=True)

    # Ensure correct types
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    df["volume"] = df["volume"].astype(int)
    for col in ["open", "high", "low", "close"]:
        df[col] = df[col].astype(float).round(4)

    # Sort by date
    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f"[TRANSFORM] ✅ Cleaned {df['ticker'].iloc[0]}: {len(df)} rows")
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add technical indicators: SMA, EMA, RSI, daily return."""
    df = df.copy()

    # Simple Moving Averages
    df["sma_20"] = df["close"].rolling(window=20).mean().round(4)
    df["sma_50"] = df["close"].rolling(window=50).mean().round(4)

    # Exponential Moving Average
    df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean().round(4)

    # Daily return %
    df["daily_return_pct"] = (df["close"].pct_change() * 100).round(4)

    # RSI (14-period)
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["rsi_14"] = (100 - (100 / (1 + rs))).round(2)

    # Bollinger Bands
    df["bb_mid"] = df["close"].rolling(20).mean()
    df["bb_upper"] = (df["bb_mid"] + 2 * df["close"].rolling(20).std()).round(4)
    df["bb_lower"] = (df["bb_mid"] - 2 * df["close"].rolling(20).std()).round(4)

    print(f"[TRANSFORM] ✅ Indicators added for {df['ticker'].iloc[0]}")
    return df


def transform_all(raw_data: dict) -> dict:
    """Run full transform pipeline on all tickers."""
    transformed = {}
    for ticker, df in raw_data.items():
        df = clean_stock_data(df)
        df = add_indicators(df)
        transformed[ticker] = df
    return transformed
