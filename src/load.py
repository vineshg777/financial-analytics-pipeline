import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

PROCESSED_DATA_PATH = Path("data/processed/sp500_processed.csv")

TABLE_NAME = "sp500_market_data"
STAGING_TABLE = "sp500_staging"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "sp500_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def connect():
    """
    Create a SQLAlchemy engine using credentials loaded from the .env file.
    """
    connection_string = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(connection_string)


def create_table(engine):
    """
    Create the target table if it does not already exist.
    """
    ddl = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        date               DATE        PRIMARY KEY,
        close              NUMERIC(12, 4),
        high               NUMERIC(12, 4),
        low                NUMERIC(12, 4),
        open               NUMERIC(12, 4),
        volume             BIGINT,
        daily_return       NUMERIC(10, 6),
        rolling_volatility NUMERIC(10, 6)
    );
    """
    with engine.connect() as conn:
        conn.execute(text(ddl))
        conn.commit()
    print(f"Table '{TABLE_NAME}' is ready.")


def load_processed_data(file_path=PROCESSED_DATA_PATH):
    """
    Load the processed CSV and normalise column names to match the database schema.
    """
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    if df.empty:
        print("The processed dataset is empty.")
        return None

    df.index.name = "date"
    df.columns = [col.lower() for col in df.columns]

    expected_columns = [
        "close", "high", "low", "open", "volume",
        "daily_return", "rolling_volatility",
    ]
    df = df[[col for col in expected_columns if col in df.columns]]

    return df


def upsert_data(df, engine):
    """
    Write data to a staging table then insert into the target table,
    skipping any dates that already exist.
    """
    df.to_sql(STAGING_TABLE, engine, if_exists="replace", index=True)

    upsert_sql = f"""
    INSERT INTO {TABLE_NAME}
        (date, close, high, low, open, volume, daily_return, rolling_volatility)
    SELECT
        date, close, high, low, open, volume, daily_return, rolling_volatility
    FROM {STAGING_TABLE}
    ON CONFLICT (date) DO NOTHING;
    """

    with engine.connect() as conn:
        conn.execute(text(upsert_sql))
        conn.execute(text(f"DROP TABLE IF EXISTS {STAGING_TABLE};"))
        conn.commit()

    print(f"Data upserted into '{TABLE_NAME}'.")


def run_loader(file_path=PROCESSED_DATA_PATH):
    """
    Run the full load step: connect to the database, ensure the table exists,
    and upsert the processed data.
    """
    engine = connect()

    create_table(engine)

    data = load_processed_data(file_path)
    if data is None:
        return None

    upsert_data(data, engine)

    print("Load step complete.")
    return data


if __name__ == "__main__":
    run_loader()
