# S&P 500 ETL Pipeline

An end-to-end ETL pipeline that extracts historical S&P 500 market data, transforms it into analysis-ready features, and loads it into a PostgreSQL database. Built as a portfolio project targeting junior data engineering roles.

## What it does

1. **Extract** — downloads historical OHLCV data for the S&P 500 (`^GSPC`) from Yahoo Finance via `yfinance`
2. **Transform** — cleans the raw data and engineers features including daily returns and 20-day rolling volatility
3. **Load** — upserts the processed dataset into a PostgreSQL table using SQLAlchemy, with `ON CONFLICT DO NOTHING` to allow safe re-runs

## Architecture

```
Yahoo Finance API
      │
      ▼
data_loader.py  ──► data/raw/sp500_data.csv
      │
      ▼
preprocessing.py ──► data/processed/sp500_processed.csv
      │
      ▼
load.py ──► PostgreSQL (sp500_market_data table)
      │
      ▼
analysis.py ──► outputs/ (charts, summary stats)
```

## Tech stack

- Python 3.13
- pandas, numpy
- yfinance
- SQLAlchemy + psycopg2
- PostgreSQL
- matplotlib

## Project structure

```
financial-analytics-pipeline/
├── data/
│   ├── raw/                  # raw CSV from Yahoo Finance
│   └── processed/            # transformed CSV ready for loading
├── notebooks/
│   └── eda.ipynb             # exploratory analysis
├── outputs/
│   └── figures/              # generated charts
├── sql/
│   └── schema.sql            # DDL + analytical queries
├── src/
│   ├── data_loader.py        # extract step
│   ├── preprocessing.py      # transform step
│   ├── load.py               # load step (PostgreSQL)
│   └── analysis.py           # summary stats and visualisations
├── .env.example              # template for DB credentials
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL credentials

Copy `.env.example` to `.env` and fill in your database details:

```bash
cp .env.example .env
```

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sp500_db
DB_USER=postgres
DB_PASSWORD=your_password
```

The `.env` file is listed in `.gitignore` and is never committed.

### 4. Run the pipeline

Run each step in order:

```bash
# Extract
python src/data_loader.py

# Transform
python src/preprocessing.py

# Load into PostgreSQL
python src/load.py

# Generate analysis outputs (optional)
python src/analysis.py
```

## Database schema

```sql
CREATE TABLE sp500_market_data (
    date               DATE        PRIMARY KEY,
    close              NUMERIC(12, 4),
    high               NUMERIC(12, 4),
    low                NUMERIC(12, 4),
    open               NUMERIC(12, 4),
    volume             BIGINT,
    daily_return       NUMERIC(10, 6),
    rolling_volatility NUMERIC(10, 6)
);
```

See `sql/schema.sql` for the full DDL and example analytical queries.

## Features engineered

| Column | Description |
|---|---|
| `daily_return` | Percentage change in closing price day-over-day |
| `rolling_volatility` | 20-day rolling standard deviation of daily returns |

## Design decisions

**Why upsert instead of truncate-and-reload?** Using `ON CONFLICT DO NOTHING` means the pipeline can be re-run at any point without duplicating rows or losing data. In a production setting this pattern supports incremental loads where only new dates are appended.

**Why SQLAlchemy over raw psycopg2?** SQLAlchemy keeps the connection logic portable — swapping PostgreSQL for another database requires changing only the connection string.

**Why environment variables for credentials?** Hardcoding database passwords in source code is a common security mistake. The `.env` pattern is the standard approach for local development.

## Next steps

- Add unit tests for the transform step
- Parametrise the date range via CLI arguments
- Extend to multiple tickers
- Schedule daily runs with Apache Airflow

## Author

Pravinesh Gowrypalan — MSc Artificial Intelligence & Data Science, Queen Mary University of London  
[LinkedIn](https://www.linkedin.com/in/pravinesh-gowrypalan-204846222/) | [GitHub](https://github.com/vineshg777)
