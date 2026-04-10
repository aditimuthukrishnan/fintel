import yfinance as yf
import pandas as pd


def fetch_stock_data(tickers: list, period: str = "1y") -> dict:
    """
    Fetch historical stock data for a list of tickers.
    Args:
        tickers: List of stock ticker symbols e.g. ["AAPL", "TSLA"]
        period: Time period - 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y
    Returns:
        Dictionary of {ticker: DataFrame}
    """
    data = {}
    for ticker in tickers:
        print(f"[EXTRACT] Fetching data for {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            if df.empty:
                print(f"[EXTRACT] WARNING: No data found for {ticker}")
                continue
            df["Ticker"] = ticker
            df.reset_index(inplace=True)
            data[ticker] = df
            print(f"[EXTRACT] ✅ {ticker}: {len(df)} rows fetched")
        except Exception as e:
            print(f"[EXTRACT] ❌ Failed to fetch {ticker}: {e}")
    return data


def fetch_stock_info(ticker: str) -> dict:
    """Fetch company metadata for a ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "ticker": ticker,
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", None),
            "country": info.get("country", "N/A"),
        }
    except Exception as e:
        print(f"[EXTRACT] Failed to fetch info for {ticker}: {e}")
        return {}
