-- =============================================================
-- Schema: sp500_market_data
-- Description: Target table for the S&P 500 ETL pipeline.
--              Stores daily OHLCV data alongside engineered
--              features calculated during the transform step.
-- =============================================================

CREATE TABLE IF NOT EXISTS sp500_market_data (
    date               DATE        PRIMARY KEY,
    close              NUMERIC(12, 4),   -- adjusted closing price
    high               NUMERIC(12, 4),   -- daily high
    low                NUMERIC(12, 4),   -- daily low
    open               NUMERIC(12, 4),   -- opening price
    volume             BIGINT,           -- shares traded
    daily_return       NUMERIC(10, 6),   -- pct change in close vs previous day
    rolling_volatility NUMERIC(10, 6)    -- 20-day rolling std dev of daily returns
);

-- Index on date is implicit via PRIMARY KEY.
-- Add additional indexes here if the table grows and query patterns change.

-- =============================================================
-- Useful analytical queries against this table
-- =============================================================

-- Most volatile trading months
SELECT
    DATE_TRUNC('month', date)      AS month,
    ROUND(AVG(rolling_volatility)::NUMERIC, 6) AS avg_volatility
FROM sp500_market_data
GROUP BY 1
ORDER BY avg_volatility DESC
LIMIT 10;

-- Annual returns: compare close at year start vs year end
WITH yearly AS (
    SELECT
        EXTRACT(YEAR FROM date) AS year,
        FIRST_VALUE(close) OVER (
            PARTITION BY EXTRACT(YEAR FROM date)
            ORDER BY date
        ) AS open_price,
        LAST_VALUE(close) OVER (
            PARTITION BY EXTRACT(YEAR FROM date)
            ORDER BY date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS close_price
    FROM sp500_market_data
)
SELECT DISTINCT
    year,
    ROUND(((close_price - open_price) / open_price * 100)::NUMERIC, 2) AS annual_return_pct
FROM yearly
ORDER BY year;

-- Worst single-day drawdowns
SELECT
    date,
    ROUND((daily_return * 100)::NUMERIC, 3) AS daily_return_pct,
    close
FROM sp500_market_data
ORDER BY daily_return ASC
LIMIT 10;
