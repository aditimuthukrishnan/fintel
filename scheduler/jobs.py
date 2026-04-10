from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from extract.fetcher import fetch_stock_data
from transform.cleaner import transform_all
from load.database import load_all

# Default tickers to track
DEFAULT_TICKERS = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]


def run_etl_pipeline(tickers: list = DEFAULT_TICKERS, period: str = "1y"):
    """Full ETL pipeline: Extract → Transform → Load."""
    print("\n" + "="*50)
    print("🚀 Starting ETL Pipeline...")
    print("="*50)

    print("\n📥 EXTRACT")
    raw_data = fetch_stock_data(tickers, period=period)

    print("\n⚙️  TRANSFORM")
    transformed_data = transform_all(raw_data)

    print("\n💾 LOAD")
    load_all(transformed_data)

    print("\n✅ ETL Pipeline Complete!")
    print("="*50 + "\n")


def start_scheduler(tickers: list = DEFAULT_TICKERS):
    """Schedule the ETL pipeline to run daily at market close (4:30 PM EST)."""
    scheduler = BlockingScheduler(timezone="America/New_York")

    scheduler.add_job(
        func=run_etl_pipeline,
        trigger=CronTrigger(hour=16, minute=30, day_of_week="mon-fri"),
        kwargs={"tickers": tickers, "period": "5d"},
        id="daily_etl",
        name="Daily Stock ETL"
    )

    print("⏰ Scheduler started — pipeline runs Mon-Fri at 4:30 PM EST")
    print("   Press Ctrl+C to stop.\n")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Scheduler stopped.")
