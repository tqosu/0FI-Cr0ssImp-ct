# scripts/ofi_visualizations.py

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def save_plot(plot_name, save_path):
    """
    Helper function to save plots to the results folder.

    Parameters:
        plot_name (str): Name of the plot file.
        save_path (str): Directory to save the plot.
    """
    os.makedirs(save_path, exist_ok=True)
    plot_path = os.path.join(save_path, plot_name)
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()
    logging.info(f"Plot saved to {plot_path}")

def plot_ofi_time_series(data, ofi_column="ofi_pca", symbol_column="symbol", time_column="ts_event", interval=None, save_path=None):
    """
    Plot the time series of OFI for all symbols and save the plot.

    Parameters:
        data (pd.DataFrame): DataFrame containing OFI data.
        ofi_column (str): Name of the OFI column.
        symbol_column (str): Name of the symbol column.
        time_column (str): Name of the time column.
        interval (str): Aggregation interval (e.g., "1s", "5s").
        save_path (str, optional): Directory to save the plot. If None, the plot is displayed.
    """
    try:
        logging.info("Plotting OFI time series...")
        plt.figure(figsize=(14, 8))
        sns.lineplot(data=data, x=time_column, y=ofi_column, hue=symbol_column, palette="viridis")
        plt.title(f"Time Series of OFI Metrics for All Symbols ({interval})")
        plt.xlabel("Time (ts_event)")
        plt.ylabel("OFI Value")
        plt.legend(title="Symbol", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        
        if save_path:
            plot_name = f"ofi_time_series_{interval}.png"
            save_plot(plot_name, save_path)
        else:
            plt.show()
        logging.info("OFI time series plot completed successfully.")
    except Exception as e:
        logging.error(f"Error in plot_ofi_time_series: {e}")
        raise

def plot_ofi_distribution(data, ofi_column="ofi_pca", symbol_column="symbol", interval=None, save_path=None):
    """
    Plot the distribution of OFI for all symbols and save the plot.

    Parameters:
        data (pd.DataFrame): DataFrame containing OFI data.
        ofi_column (str): Name of the OFI column.
        symbol_column (str): Name of the symbol column.
        interval (str): Aggregation interval (e.g., "1s", "5s").
        save_path (str, optional): Directory to save the plot. If None, the plot is displayed.
    """
    try:
        logging.info("Plotting OFI distribution...")
        plt.figure(figsize=(14, 8))
        sns.histplot(data=data, x=ofi_column, hue=symbol_column, kde=True, palette="viridis", element="step", common_norm=False)
        plt.title(f"Distribution of OFI Metrics for All Symbols ({interval})")
        plt.xlabel("OFI Value")
        plt.ylabel("Frequency")
        plt.legend(title="Symbol", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        
        if save_path:
            plot_name = f"ofi_distribution_{interval}.png"
            save_plot(plot_name, save_path)
        else:
            plt.show()
        logging.info("OFI distribution plot completed successfully.")
    except Exception as e:
        logging.error(f"Error in plot_ofi_distribution: {e}")
        raise

def plot_ofi_heatmap(data, ofi_column="ofi_pca", symbol_column="symbol", time_column="ts_event", interval=None, save_path=None):
    """
    Plot a heatmap of OFI across time and symbols and save the plot.

    Parameters:
        data (pd.DataFrame): DataFrame containing OFI data.
        ofi_column (str): Name of the OFI column.
        symbol_column (str): Name of the symbol column.
        time_column (str): Name of the time column.
        interval (str): Aggregation interval (e.g., "1s", "5s").
        save_path (str, optional): Directory to save the plot. If None, the plot is displayed.
    """
    try:
        logging.info("Plotting OFI heatmap...")
        ofi_matrix = data.pivot(index=time_column, columns=symbol_column, values=ofi_column)
        plt.figure(figsize=(14, 8))
        sns.heatmap(ofi_matrix, cmap="viridis", cbar_kws={"label": "OFI Value"})
        plt.title(f"Heatmap of OFI Metrics Across Time and Symbols ({interval})")
        plt.xlabel("Symbol")
        plt.ylabel("Time (ts_event)")
        plt.tight_layout()
        
        if save_path:
            plot_name = f"ofi_heatmap_{interval}.png"
            save_plot(plot_name, save_path)
        else:
            plt.show()
        logging.info("OFI heatmap plot completed successfully.")
    except Exception as e:
        logging.error(f"Error in plot_ofi_heatmap: {e}")
        raise

def plot_ofi_boxplot(data, ofi_column="ofi_pca", symbol_column="symbol", interval=None, save_path=None):
    """
    Plot a boxplot of OFI for all symbols and save the plot.

    Parameters:
        data (pd.DataFrame): DataFrame containing OFI data.
        ofi_column (str): Name of the OFI column.
        symbol_column (str): Name of the symbol column.
        interval (str): Aggregation interval (e.g., "1s", "5s").
        save_path (str, optional): Directory to save the plot. If None, the plot is displayed.
    """
    try:
        logging.info("Plotting OFI boxplot...")
        plt.figure(figsize=(14, 8))
        sns.boxplot(data=data, x=symbol_column, y=ofi_column, palette="viridis")
        plt.title(f"Boxplot of OFI Metrics for All Symbols ({interval})")
        plt.xlabel("Symbol")
        plt.ylabel("OFI Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plot_name = f"ofi_boxplot_{interval}.png"
            save_plot(plot_name, save_path)
        else:
            plt.show()
        logging.info("OFI boxplot plot completed successfully.")
    except Exception as e:
        logging.error(f"Error in plot_ofi_boxplot: {e}")
        raise