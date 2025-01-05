from sklearn.decomposition import PCA
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def integrate_ofi_with_pca(order_book_data, levels=5):
    """
    Integrate multi-level OFI metrics into a single metric using PCA.

    Parameters:
        order_book_data (pd.DataFrame): DataFrame containing order book data with OFI columns.
        levels (int): Number of levels in the order book.

    Returns:
        pd.DataFrame: DataFrame with an additional column 'ofi_pca' containing the integrated OFI metric.
    """
    try:
        logging.info("Integrating OFI using PCA...")
        # Extract OFI columns
        ofi_columns = [f"of_{level}_b" for level in range(levels)] + [f"of_{level}_a" for level in range(levels)]
        ofi_data = order_book_data[ofi_columns]

        # Apply PCA
        pca = PCA(n_components=1)
        order_book_data["ofi_pca"] = pca.fit_transform(ofi_data)

        logging.info("OFI integration using PCA completed successfully.")
        return order_book_data

    except Exception as e:
        logging.error(f"Error in integrate_ofi_with_pca: {e}")
        raise
