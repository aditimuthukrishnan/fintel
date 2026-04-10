import pandas as pd # type: ignore
import plotly.graph_objects as go # type: ignore
from plotly.subplots import make_subplots # type: ignore
from load.database import query_db # type: ignore


def plot_price_and_volume(ticker: str):
    """Candlestick chart with volume bars."""
    df = query_db(f"SELECT * FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date")

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.7, 0.3],
                        subplot_titles=[f"{ticker} Price", "Volume"])

    fig.add_trace(go.Candlestick(
        x=df["date"], open=df["open"], high=df["high"],
        low=df["low"], close=df["close"], name="Price"
    ), row=1, col=1)

    fig.add_trace(go.Bar(x=df["date"], y=df["volume"], name="Volume", marker_color="steelblue"), row=2, col=1)

    fig.update_layout(title=f"{ticker} — Price & Volume", xaxis_rangeslider_visible=False, height=600)
    fig.show()


def plot_moving_averages(ticker: str):
    """Close price with SMA20, SMA50, EMA20."""
    df = query_db(f"SELECT * FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["close"], name="Close", line=dict(color="white", width=1)))
    fig.add_trace(go.Scatter(x=df["date"], y=df["sma_20"], name="SMA 20", line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=df["date"], y=df["sma_50"], name="SMA 50", line=dict(color="cyan")))
    fig.add_trace(go.Scatter(x=df["date"], y=df["ema_20"], name="EMA 20", line=dict(color="lime", dash="dot")))

    fig.update_layout(title=f"{ticker} — Moving Averages", template="plotly_dark", height=500)
    fig.show()


def plot_rsi(ticker: str):
    """RSI chart with overbought/oversold lines."""
    df = query_db(f"SELECT * FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["rsi_14"], name="RSI 14", line=dict(color="violet")))
    fig.add_hline(y=70, line_color="red", line_dash="dash", annotation_text="Overbought")
    fig.add_hline(y=30, line_color="green", line_dash="dash", annotation_text="Oversold")

    fig.update_layout(title=f"{ticker} — RSI (14)", template="plotly_dark", height=400, yaxis=dict(range=[0, 100]))
    fig.show()


def plot_bollinger_bands(ticker: str):
    """Close price with Bollinger Bands."""
    df = query_db(f"SELECT * FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["bb_upper"], name="Upper Band", line=dict(color="red", dash="dot")))
    fig.add_trace(go.Scatter(x=df["date"], y=df["close"], name="Close", line=dict(color="white")))
    fig.add_trace(go.Scatter(x=df["date"], y=df["bb_lower"], name="Lower Band", line=dict(color="green", dash="dot"),
                             fill="tonexty", fillcolor="rgba(0,255,0,0.05)"))

    fig.update_layout(title=f"{ticker} — Bollinger Bands", template="plotly_dark", height=500)
    fig.show()


def plot_returns_comparison(tickers: list):
    """Compare cumulative returns of multiple tickers."""
    fig = go.Figure()
    for ticker in tickers:
        df = query_db(f"SELECT date, close FROM stock_prices WHERE ticker = '{ticker}' ORDER BY date")
        df["cumulative_return"] = (df["close"] / df["close"].iloc[0] - 1) * 100
        fig.add_trace(go.Scatter(x=df["date"], y=df["cumulative_return"], name=ticker))

    fig.update_layout(title="Cumulative Returns Comparison (%)", template="plotly_dark",
                      yaxis_title="Return (%)", height=500)
    fig.show()
