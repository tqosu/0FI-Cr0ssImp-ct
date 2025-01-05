# scripts/cross_impact.py

import pandas as pd
from sklearn.linear_model import LassoCV
import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def contemporaneous_cross_impact(merged_data):
    """
    Analyze contemporaneous cross-impact using LASSO regression.

    Parameters:
        merged_data (pd.DataFrame): DataFrame containing OFI and returns data.
            Expected columns: 'ts_event', 'symbol', 'ofi_pca', 'log_return'.

    Returns:
        pd.DataFrame: Cross-impact coefficients, where rows are target stocks and columns are predictor stocks.
    """
    try:
        logging.info("Analyzing contemporaneous cross-impact...")

        # Step 1: Pivot OFI data
        ofi_matrix = merged_data.pivot(index="ts_event", columns="symbol", values="ofi_pca")

        # Step 2: Pivot returns data
        returns_matrix = merged_data.pivot(index="ts_event", columns="symbol", values="log_return")

        # Step 3: Initialize a DataFrame to store cross-impact coefficients
        cross_impact_coef = pd.DataFrame(index=returns_matrix.columns, columns=ofi_matrix.columns)

        # Step 4: Perform LASSO regression for each stock
        for target_stock in returns_matrix.columns:
            y = returns_matrix[target_stock].dropna()  # Returns of the target stock
            X = ofi_matrix.loc[y.index].fillna(0)     # OFI of all stocks (including itself)

            # Standardize features (handle zero standard deviation)
            X_mean = X.mean()
            X_std = X.std()

            # Replace zero standard deviation with a small value to avoid division by zero
            X_std[X_std == 0] = 1e-10

            # Standardize X
            X = (X - X_mean) / X_std

            # Fit LASSO regression with cross-validation
            lasso = LassoCV(cv=5, max_iter=2000, tol=1e-4)
            lasso.fit(X, y)

            # Store coefficients
            cross_impact_coef.loc[target_stock] = lasso.coef_

        logging.info("Contemporaneous cross-impact analysis completed successfully.")
        return cross_impact_coef

    except Exception as e:
        logging.error(f"Error in contemporaneous_cross_impact: {e}")
        raise

def preprocess_data(merged_data):
    """
    Preprocess the data to handle duplicates based on context.

    Parameters:
        merged_data (pd.DataFrame): DataFrame containing OFI and returns data.

    Returns:
        pd.DataFrame: Preprocessed data.
    """
    try:
        logging.info("Preprocessing data...")

        # Check for duplicates
        duplicates = merged_data[merged_data.duplicated(subset=["ts_event", "symbol"], keep=False)]
        if not duplicates.empty:
            logging.warning("Duplicate entries found. Handling based on context.")

            # Example: Drop rows with action=C if analyzing trades
            # merged_data = merged_data[merged_data["action"] == "T"]

            # Alternatively, aggregate duplicates
            merged_data = merged_data.groupby(["ts_event", "symbol"], as_index=False).agg({
                "ofi_pca": "mean",
                "log_return": "mean",
                "mid_price": "mean"
            })

        logging.info("Data preprocessing completed successfully.")
        return merged_data

    except Exception as e:
        logging.error(f"Error in preprocess_data: {e}")
        raise