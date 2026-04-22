from pathlib import Path

import matplotlib
import pandas as pd


matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROCESSED_DATA_PATH = Path("data/processed/sp500_processed.csv")
OUTPUT_DIR = Path("outputs/figures")
SUMMARY_OUTPUT_PATH = Path("outputs/summary_statistics.csv")


def load_processed_data(file_path=PROCESSED_DATA_PATH):
    """
    Load the processed S&P 500 dataset.
    """
    df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")

    if df.empty:
        print("The processed dataset is empty.")
        return None

    return df


def calculate_cumulative_returns(df):
    """
    Add a cumulative return column so we can track growth over time.
    """
    df = df.copy()
    df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod() - 1
    return df


def calculate_drawdown(df):
    """
    Add drawdown columns to measure declines from previous portfolio peaks.
    """
    df = df.copy()
    cumulative_growth = (1 + df["Daily_Return"]).cumprod()
    running_peak = cumulative_growth.cummax()

    df["Cumulative_Growth"] = cumulative_growth
    df["Drawdown"] = (cumulative_growth / running_peak) - 1

    return df


def generate_summary_statistics(df):
    """
    Create a set of portfolio-style return and risk metrics.
    """
    trading_days = 252
    average_daily_return = df["Daily_Return"].mean()
    daily_return_std = df["Daily_Return"].std()
    annualized_return = average_daily_return * trading_days
    annualized_volatility = daily_return_std * (trading_days ** 0.5)
    sharpe_ratio = (
        annualized_return / annualized_volatility
        if annualized_volatility != 0
        else pd.NA
    )

    summary = pd.Series(
        {
            "Start Date": df.index.min().date(),
            "End Date": df.index.max().date(),
            "Average Daily Return": average_daily_return,
            "Daily Return Std Dev": daily_return_std,
            "Annualised Return": annualized_return,
            "Annualised Volatility": annualized_volatility,
            "Sharpe Ratio (rf=0)": sharpe_ratio,
            "Average Rolling Volatility": df["Rolling_Volatility"].mean(),
            "Best Daily Return": df["Daily_Return"].max(),
            "Worst Daily Return": df["Daily_Return"].min(),
            "Total Cumulative Return": df["Cumulative_Return"].iloc[-1],
            "Maximum Drawdown": df["Drawdown"].min(),
        }
    )

    return summary


def save_summary_statistics(summary, output_path=SUMMARY_OUTPUT_PATH):
    """
    Save summary statistics so they can be reused outside the terminal.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, header=["Value"])
    print(f"Summary statistics saved to {output_path}")


def plot_closing_price(df, output_dir=OUTPUT_DIR):
    """
    Plot the S&P 500 closing price over time.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], color="navy", linewidth=1.8)
    plt.title("S&P 500 Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Index Level")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "sp500_closing_price.png")
    plt.close()


def plot_daily_returns(df, output_dir=OUTPUT_DIR):
    """
    Plot daily returns to show how often the market moves up or down.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Daily_Return"], color="darkgreen", linewidth=1)
    plt.axhline(0, color="black", linestyle="--", linewidth=1)
    plt.title("S&P 500 Daily Returns")
    plt.xlabel("Date")
    plt.ylabel("Daily Return")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "sp500_daily_returns.png")
    plt.close()


def plot_rolling_volatility(df, output_dir=OUTPUT_DIR):
    """
    Plot rolling volatility to show how market risk changes over time.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Rolling_Volatility"], color="firebrick", linewidth=1.5)
    plt.title("S&P 500 20-Day Rolling Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "sp500_rolling_volatility.png")
    plt.close()


def plot_drawdown(df, output_dir=OUTPUT_DIR):
    """
    Plot drawdown to highlight the size of declines from prior highs.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Drawdown"], color="darkorange", linewidth=1.5)
    plt.axhline(0, color="black", linestyle="--", linewidth=1)
    plt.title("S&P 500 Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "sp500_drawdown.png")
    plt.close()


def run_analysis(
    input_path=PROCESSED_DATA_PATH,
    output_dir=OUTPUT_DIR,
    summary_output_path=SUMMARY_OUTPUT_PATH,
):
    """
    Run the full analysis workflow.
    """
    data = load_processed_data(input_path)

    if data is None:
        return None

    data = calculate_cumulative_returns(data)
    data = calculate_drawdown(data)
    summary = generate_summary_statistics(data)
    save_summary_statistics(summary, summary_output_path)

    plot_closing_price(data, output_dir)
    plot_daily_returns(data, output_dir)
    plot_rolling_volatility(data, output_dir)
    plot_drawdown(data, output_dir)

    print("Summary statistics:")
    print(summary)

    return data, summary


if __name__ == "__main__":
    run_analysis()
