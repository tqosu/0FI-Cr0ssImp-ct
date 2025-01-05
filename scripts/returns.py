# scripts/returns.py

import numpy as np
import logging, os
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def calculate_log_returns(order_book_data):
    """
    Calculate logarithmic returns based on the mid-price (average of best bid and ask prices).

    Parameters:
        order_book_data (pd.DataFrame): DataFrame containing order book data with 'bid_px_00' and 'ask_px_00' columns.

    Returns:
        pd.DataFrame: Logarithmic returns with 'ts_event' and 'symbol' columns.
    """
    try:
        logging.info("Calculating logarithmic returns using mid-price...")

        # Step 1: Validate input columns
        required_columns = ["symbol", "ts_event", "bid_px_00", "ask_px_00"]
        if not all(col in order_book_data.columns for col in required_columns):
            raise ValueError(f"Input DataFrame must contain the following columns: {required_columns}")

        # Step 2: Calculate mid-price as the average of best bid and ask prices
        order_book_data["mid_price"] = (order_book_data["bid_px_00"] + order_book_data["ask_px_00"]) / 2

        # Step 3: Group by symbol and calculate log returns
        log_returns = order_book_data.groupby("symbol").apply(
            lambda x: x.assign(log_return=np.log(x["mid_price"] / x["mid_price"].shift(1)))
        ).reset_index(drop=True)

        # Step 4: Handle potential NaN or inf values
        log_returns["log_return"].replace([np.inf, -np.inf], np.nan, inplace=True)

        # Step 5: Drop rows with NaN log returns (optional, depending on your use case)
        log_returns = log_returns.dropna(subset=["log_return"])

        logging.info("Logarithmic returns calculated successfully.")
        return log_returns[["symbol", "ts_event", "log_return"]]

    except Exception as e:
        logging.error(f"Error in calculate_log_returns: {e}")
        raise


import seaborn as sns
import matplotlib.pyplot as plt

def plot_log_return_time_series(data, interval=None, save_path=None):
    """
    Plot the time series of log_return for all symbols in the same plot.

    Parameters:
        data (pd.DataFrame): DataFrame containing 'symbol', 'ts_event', and 'log_return' columns.
        interval (str, optional): Aggregation interval (e.g., "1s", "5s"). If provided, it will be included in the plot title and filename.
        save_path (str, optional): Directory to save the plot. If None, the plot is displayed.
    """
    try:
        logging.info("Plotting log return time series...")

        # Validate input columns
        required_columns = ["symbol", "ts_event", "log_return"]
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Input DataFrame must contain the following columns: {required_columns}")

        # Create the plot
        plt.figure(figsize=(14, 8))
        sns.lineplot(data=data, x="ts_event", y="log_return", hue="symbol", palette="viridis")
        
        # Include interval in the title if provided
        title = f"Time Series of Log Returns for All Symbols ({interval})" if interval else "Time Series of Log Returns for All Symbols"
        plt.title(title)
        
        plt.xlabel("Time (ts_event)")
        plt.ylabel("Log Return")
        plt.legend(title="Symbol", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        
        # Save the plot if save_path is provided
        if save_path:
            plot_name = f"log_return_time_series_{interval}.png" if interval else "log_return_time_series.png"
            full_path = os.path.join(save_path, plot_name)
            plt.savefig(full_path, bbox_inches="tight")
            logging.info(f"Plot saved to {full_path}")
        else:
            plt.show()
        plt.close()
        logging.info("Log return time series plot completed successfully.")

    except Exception as e:
        logging.error(f"Error in plot_log_return_time_series: {e}")
        raise