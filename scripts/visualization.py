# scripts/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import logging
import os
import pandas as pd

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

def plot_heatmap(cross_impact_coef, title, interval, save_path=None):
    """
    Plot a heatmap of cross-impact coefficients.

    Parameters:
        cross_impact_coef (pd.DataFrame): Cross-impact coefficients.
        title (str): Title of the plot.
        interval (str): Aggregation interval (e.g., "1s", "5s").
        save_path (str, optional): Path to save the plot. If None, the plot is displayed.
    """
    try:
        logging.info(f"Plotting heatmap: {title}")

        # Ensure all values are numeric
        cross_impact_coef = cross_impact_coef.apply(pd.to_numeric, errors="coerce")
        
        # Fill NaN values with 0 (or handle them as needed)
        cross_impact_coef = cross_impact_coef.fillna(0)

        plt.figure(figsize=(10, 8))
        sns.heatmap(cross_impact_coef, cmap="coolwarm", center=0, annot=True, fmt=".2f")
        plt.title(title)
        plt.xlabel("OFI (Predictor Stocks)")
        plt.ylabel("Returns (Target Stocks)")
        
        if save_path:
            # Include interval in the filename
            plot_name = f"cross_impact_heatmap_{interval}.png"
            full_path = os.path.join(save_path, plot_name)
            plt.savefig(full_path, bbox_inches="tight")
            logging.info(f"Heatmap saved to {full_path}")
        else:
            plt.show()
        plt.close()
        logging.info("Heatmap plotted successfully.")

    except Exception as e:
        logging.error(f"Error in plot_heatmap: {e}")
        raise
        
def compare_self_vs_cross_impact(cross_impact_coef, title, interval, save_path=None):
    """
    Compare self-impact vs. cross-impact for a given cross-impact coefficient matrix.

    Parameters:
        cross_impact_coef (pd.DataFrame): Cross-impact coefficients.
        title (str): Title of the plot.
        interval (str): Aggregation interval (e.g., "1s", "5s").
        save_path (str, optional): Path to save the plot. If None, the plot is displayed.
    """
    try:
        logging.info(f"Comparing self-impact vs. cross-impact: {title}")

        # Ensure all values are numeric
        cross_impact_coef = cross_impact_coef.apply(pd.to_numeric, errors="coerce")
        
        # Fill NaN values with 0 (or handle them as needed)
        cross_impact_coef = cross_impact_coef.fillna(0)

        # Extract self-impact (diagonal elements) and cross-impact (off-diagonal elements)
        self_impact = np.diag(cross_impact_coef)
        cross_impact = cross_impact_coef.values - np.diag(self_impact)
        
        # Calculate average cross-impact for each target stock
        avg_cross_impact = cross_impact.mean(axis=1)

        plt.figure(figsize=(8, 6))
        plt.scatter(self_impact, avg_cross_impact, alpha=0.5)
        plt.title(title)
        plt.xlabel("Self-Impact")
        plt.ylabel("Average Cross-Impact")
        
        if save_path:
            # Include interval in the filename
            plot_name = f"self_vs_cross_impact_{interval}.png"
            full_path = os.path.join(save_path, plot_name)
            plt.savefig(full_path, bbox_inches="tight")
            logging.info(f"Comparison plot saved to {full_path}")
        else:
            plt.show()
        plt.close()
        logging.info("Comparison plot completed successfully.")

    except Exception as e:
        logging.error(f"Error in compare_self_vs_cross_impact: {e}")
        raise