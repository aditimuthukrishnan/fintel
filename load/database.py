import pandas as pd
from sqlalchemy import create_engine, text
import os


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/stocks.db")


def get_engine():
    """Create and return SQLAlchemy engine."""
    return create_engine(f"sqlite:///{DB_PATH}")


def load_to_db(df: pd.DataFrame, table_name: str = "stock_prices", if_exists: str = "append"):
    """
    Load a DataFrame into the SQLite database.
    Args:
        df: Transformed stock DataFrame
        table_name: Target table name
        if_exists: 'append', 'replace', or 'fail'
    """
    engine = get_engine()
    ticker = df["ticker"].iloc[0]

    try:
        with engine.connect() as conn:
            if if_exists == "append":
                # Avoid duplicate rows by deleting existing ticker data first
                conn.execute(text(f"DELETE FROM {table_name} WHERE ticker = '{ticker}'"))
                conn.commit()
    except Exception:
        pass  # Table doesn't exist yet, that's fine

    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    print(f"[LOAD] ✅ {ticker}: {len(df)} rows loaded into '{table_name}'")


def load_all(transformed_data: dict):
    """Load all transformed ticker data into DB."""
    for ticker, df in transformed_data.items():
        load_to_db(df)


def query_db(sql: str) -> pd.DataFrame:
    """Run a raw SQL query and return results as DataFrame."""
    engine = get_engine()
    return pd.read_sql(sql, engine)
