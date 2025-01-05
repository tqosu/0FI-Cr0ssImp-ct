# scripts/ofi_calculation.py

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def calculate_order_flows(order_book_data, levels=5):
    """
    Calculate bid and ask order flows at each level of the limit order book.

    Parameters:
        order_book_data (pd.DataFrame): DataFrame containing order book data.
        levels (int): Number of levels in the order book.

    Returns:
        pd.DataFrame: DataFrame with added OFI columns.
    """
    try:
        logging.info("Calculating order flows...")

        # Validate input columns
        required_columns = ["symbol", "ts_event"]
        for level in range(levels):
            required_columns.extend([f"bid_px_{level:02d}", f"ask_px_{level:02d}", f"bid_sz_{level:02d}", f"ask_sz_{level:02d}"])
        
        if not all(col in order_book_data.columns for col in required_columns):
            raise ValueError(f"Input DataFrame must contain the following columns: {required_columns}")

        # Initialize a list to store processed groups
        processed_groups = []

        # Step 1: Process each symbol
        for symbol, group in order_book_data.groupby("symbol"):
            logging.info(f"Processing symbol: {symbol}")
            group = group.sort_values(by="ts_event")

            # Step 2: Calculate OFI for each level
            for level in range(levels):
                bid_px_col = f"bid_px_{level:02d}"
                ask_px_col = f"ask_px_{level:02d}"
                bid_sz_col = f"bid_sz_{level:02d}"
                ask_sz_col = f"ask_sz_{level:02d}"

                # Compute shifted values for bid and ask prices and sizes
                group[f"{bid_px_col}_prev"] = group[bid_px_col].shift(1)
                group[f"{bid_sz_col}_prev"] = group[bid_sz_col].shift(1)
                group[f"{ask_px_col}_prev"] = group[ask_px_col].shift(1)
                group[f"{ask_sz_col}_prev"] = group[ask_sz_col].shift(1)

                # Compute bid order flows
                group[f"of_{level}_b"] = np.where(
                    group[bid_px_col] > group[f"{bid_px_col}_prev"], group[bid_sz_col],  # Case 1: Bid price increases
                    np.where(
                        group[bid_px_col] == group[f"{bid_px_col}_prev"], group[bid_sz_col] - group[f"{bid_sz_col}_prev"],  # Case 2: Bid price unchanged
                        -group[bid_sz_col]  # Case 3: Bid price decreases
                    )
                )

                # Compute ask order flows
                group[f"of_{level}_a"] = np.where(
                    group[ask_px_col] > group[f"{ask_px_col}_prev"], -group[ask_sz_col],  # Case 1: Ask price increases
                    np.where(
                        group[ask_px_col] == group[f"{ask_px_col}_prev"], group[ask_sz_col] - group[f"{ask_sz_col}_prev"],  # Case 2: Ask price unchanged
                        group[ask_sz_col]  # Case 3: Ask price decreases
                    )
                )

            # Step 3: Drop temporary columns
            columns_to_drop = [
                col
                for level in range(levels)
                for col in [
                    f"bid_px_{level:02d}_prev",
                    f"bid_sz_{level:02d}_prev",
                    f"ask_px_{level:02d}_prev",
                    f"ask_sz_{level:02d}_prev",
                ]
            ]
            group.drop(columns=columns_to_drop, inplace=True)

            # Append the processed group to the list
            processed_groups.append(group)

        # Step 4: Combine all processed groups into a single DataFrame
        result = pd.concat(processed_groups, ignore_index=True)
        logging.info("Order flow calculation completed.")
        return result

    except Exception as e:
        logging.error(f"Error in calculate_order_flows: {e}")
        raise

def aggregate_order_book_data(order_book_data, levels=6, interval="1S"):
    """
    Aggregate order book data by a specified time interval, handling multiple levels.

    Parameters:
        order_book_data (pd.DataFrame): Raw order book data.
        levels (int): Number of levels in the order book (e.g., 6 for levels 0 to 5).
        interval (str): Time interval for aggregation (e.g., "1S" for 1 second).

    Returns:
        pd.DataFrame: Aggregated order book data.
    """
    try:
        logging.info(f"Aggregating order book data by {interval}...")

        # Ensure ts_event is in datetime format
        if not np.issubdtype(order_book_data["ts_event"].dtype, np.datetime64):
            order_book_data["ts_event"] = pd.to_datetime(order_book_data["ts_event"], unit="s")

        # Set ts_event as the index
        order_book_data = order_book_data.set_index("ts_event")

        # Define aggregation rules for each column
        aggregation_rules = {}
        for level in range(levels):
            # Add rules for bid/ask prices and sizes at each level
            aggregation_rules[f"bid_px_{level:02d}"] = "last"  # Use the last bid price
            aggregation_rules[f"ask_px_{level:02d}"] = "last"  # Use the last ask price
            aggregation_rules[f"bid_sz_{level:02d}"] = "sum"   # Sum bid sizes
            aggregation_rules[f"ask_sz_{level:02d}"] = "sum"   # Sum ask sizes

        # Add rules for other columns (e.g., action, side)
        aggregation_rules["action"] = "last"  # Use the last action
        aggregation_rules["side"] = "last"    # Use the last side
        aggregation_rules["price"] = "last"    # Use the last side

        # Group by symbol and resample by the specified interval
        aggregated_data = (
            order_book_data.groupby("symbol")
            .resample(interval)
            .agg(aggregation_rules)
            .reset_index()
        )

        logging.info("Order book data aggregation completed successfully.")
        return aggregated_data

    except Exception as e:
        logging.error(f"Error in aggregate_order_book_data: {e}")
        raise
