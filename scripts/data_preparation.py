import databento as db
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def download_databento_data(api_key, symbols, start_time, end_time, dataset="XNAS.ITCH", schema="mbp-10", output_file="order_book_trades_15min.csv"):
    """
    Download order book and trade data from Databento.

    Parameters:
        api_key (str): Your Databento API key.
        symbols (list): List of stock symbols to download.
        start_time (str): Start time in "YYYY-MM-DDTHH:MM:SS" format.
        end_time (str): End time in "YYYY-MM-DDTHH:MM:SS" format.
        dataset (str): Dataset name (default: "XNAS.ITCH" for Nasdaq ITCH).
        schema (str): Data schema (default: "mbp-10" for order book and trades).
        output_file (str): Output CSV file name (default: "order_book_trades_15min.csv").

    Returns:
        None
    """
    try:
        logging.info("Initializing Databento client...")
        client = db.Historical(api_key)

        logging.info(f"Downloading data for symbols: {symbols}")
        data = client.timeseries.get_range(
            dataset=dataset,
            start=start_time,
            end=end_time,
            symbols=symbols,
            schema=schema,
            stype_in="native",  # Use native symbology
        )

        logging.info(f"Saving data to {output_file}...")
        data.to_csv(output_file)

        logging.info("Data retrieval complete.")

    except Exception as e:
        logging.error(f"Error in download_databento_data: {e}")
        raise

# Example usage
if __name__ == "__main__":
    # Set your API key
    API_KEY = "YOUR_API_KEY"  # Replace with your Databento API key

    # Define the stocks and time range
    SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMGN", "GILD", "TSLA", "PEP", "JPM", "V", "XOM"]
    START = "2025-01-03T10:30:00"  # Start time
    END = "2025-01-03T10:45:00"    # End time

    # Download data
    download_databento_data(api_key=API_KEY, symbols=SYMBOLS, start_time=START, end_time=END)
