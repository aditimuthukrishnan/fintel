import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
from scheduler.jobs import run_etl_pipeline, start_scheduler
from visualize.charts import (
    plot_price_and_volume,
    plot_moving_averages,
    plot_rsi,
    plot_bollinger_bands,
    plot_returns_comparison,
)

DEFAULT_TICKERS = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]


def main():
    parser = argparse.ArgumentParser(description="Stock Market ETL Pipeline")
    parser.add_argument("--tickers", nargs="+", default=DEFAULT_TICKERS)
    parser.add_argument("--period", default="1y")
    parser.add_argument("--schedule", action="store_true")
    parser.add_argument("--charts", metavar="TICKER")
    parser.add_argument("--compare", action="store_true")

    args = parser.parse_args()

    if args.schedule:
        start_scheduler(tickers=args.tickers)
    elif args.charts:
        ticker = args.charts.upper()
        print(f"📊 Showing charts for {ticker}...")
        plot_price_and_volume(ticker)
        plot_moving_averages(ticker)
        plot_rsi(ticker)
        plot_bollinger_bands(ticker)
    elif args.compare:
        plot_returns_comparison(args.tickers)
    else:
        run_etl_pipeline(tickers=args.tickers, period=args.period)


if __name__ == "__main__":
    main()