# 📈 Stock Market ETL Pipeline

A Python ETL pipeline that extracts real stock market data, transforms it with technical indicators, stores it in a database, and visualizes it with interactive charts.

## 🚀 Features

- **Extract** — Pulls historical OHLCV data from Yahoo Finance (free, no API key needed)
- **Transform** — Cleans data and calculates SMA, EMA, RSI, Bollinger Bands, daily returns
- **Load** — Stores everything in a local SQLite database
- **Visualize** — Interactive candlestick, RSI, MA, and returns charts via Plotly
- **Scheduler** — Runs automatically every weekday at 4:30 PM EST

## 🛠️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR-USERNAME/stock-etl-pipeline.git
cd stock-etl-pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline
python main.py
```

## 📖 Usage

```bash
# Run ETL with default tickers (AAPL, TSLA, GOOGL, MSFT, AMZN)
python main.py

# Run with custom tickers
python main.py --tickers NVDA META NFLX --period 6mo

# Show interactive charts for a ticker
python main.py --charts AAPL

# Compare cumulative returns across tickers
python main.py --compare --tickers AAPL TSLA NVDA

# Start daily auto-scheduler (runs Mon-Fri at 4:30 PM EST)
python main.py --schedule
```

## 📁 Project Structure

```
stock-etl-pipeline/
├── extract/
│   └── fetcher.py       # Pulls data from Yahoo Finance
├── transform/
│   └── cleaner.py       # Cleans data + adds indicators
├── load/
│   └── database.py      # Saves to SQLite via SQLAlchemy
├── visualize/
│   └── charts.py        # Interactive Plotly charts
├── scheduler/
│   └── jobs.py          # APScheduler daily pipeline
├── data/
│   └── stocks.db        # SQLite database (auto-created)
├── main.py              # Entry point
└── requirements.txt
```

## 📊 Technical Indicators

| Indicator | Description |
|-----------|-------------|
| SMA 20/50 | Simple Moving Average |
| EMA 20    | Exponential Moving Average |
| RSI 14    | Relative Strength Index |
| Bollinger Bands | Volatility bands (20-period) |
| Daily Return % | Day-over-day % change |

## 🧰 Tech Stack

- `yfinance` — Free stock data
- `pandas` — Data processing
- `sqlalchemy` — Database ORM
- `plotly` — Interactive charts
- `APScheduler` — Job scheduling
