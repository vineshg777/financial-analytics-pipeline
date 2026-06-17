# Financial Analytics Pipeline

A portfolio project that downloads, preprocesses and analyses S&P 500 market data using Python.

This project is designed to show a practical data workflow that is relevant for data analyst, data science, and fintech roles. It covers data collection, feature engineering, basic risk analysis, and output generation in a clean project structure.

## Project Goal

The goal of this project is to build a simple but professional financial data pipeline that:

- downloads historical S&P 500 data
- cleans and transforms raw market data
- calculates daily returns and rolling volatility
- measures performance and downside risk
- generates summary statistics and charts
- saves outputs in a reusable format

## Tech Stack

- Python 3.13
- pandas
- numpy
- matplotlib
- scikit-learn
- yfinance
- Jupyter

## Project Structure

```text
financial-analytics-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── eda.ipynb
├── outputs/
│   └── figures/
├── sql/
│   └── queries.sql
├── src/
│   ├── analysis.py
│   ├── data_loader.py
│   └── preprocessing.py
├── README.md
└── requirements.txt
```

## Workflow

### 1. Data Loading

[`src/data_loader.py`](src/data_loader.py) downloads historical S&P 500 data from Yahoo Finance using the `^GSPC` ticker and saves it to:

`data/raw/sp500_data.csv`

### 2. Preprocessing

[`src/preprocessing.py`](src/preprocessing.py) loads the raw CSV file, then:

- calculates daily returns from the closing price
- calculates 20-day rolling volatility
- removes missing values created during feature engineering
- saves the cleaned dataset to:

`data/processed/sp500_processed.csv`

### 3. Analysis

[`src/analysis.py`](src/analysis.py) loads the processed dataset, calculates cumulative returns and drawdowns, prints summary statistics, saves a metrics table, and exports charts to:

`outputs/figures/`

It also saves summary metrics to:

`outputs/summary_statistics.csv`

Generated charts:

- S&P 500 closing price over time
- daily returns over time
- 20-day rolling volatility over time
- drawdown over time

## Example Features Created

The processed dataset includes:

- `Close`: daily closing price of the S&P 500
- `Daily_Return`: percentage change in closing price from one day to the next
- `Rolling_Volatility`: 20-day rolling standard deviation of returns
- `Cumulative_Return`: total compounded return over time during analysis
- `Drawdown`: percentage decline from the previous cumulative peak

## How To Run

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the pipeline step by step

Download raw data:

```bash
python src/data_loader.py
```

Preprocess the raw data:

```bash
python src/preprocessing.py
```

Run the analysis:

```bash
python src/analysis.py
```

## Current Outputs

After running the scripts, the project produces:

- raw market data in CSV format
- processed market data with engineered features
- saved charts for price, return, volatility, and drawdown analysis
- summary statistics printed in the terminal
- a reusable summary metrics CSV for reporting or dashboards

## Why This Project Matters

This project demonstrates several skills that are useful in data and fintech roles:

- working with external financial data APIs
- building a multi-step data pipeline
- transforming raw market data into usable features
- analysing returns, volatility, and drawdowns
- computing portfolio-style metrics such as annualised return, annualised volatility, Sharpe ratio, and maximum drawdown
- organising a project in a professional repository structure

## Next Improvements

Possible next steps for the project:

- compare S&P 500 performance across time periods
- build a dashboard version of the analysis
- add unit tests for each pipeline step
- expand to multiple tickers instead of only the S&P 500

## Author

Built as a portfolio project for data and fintech job applications.
