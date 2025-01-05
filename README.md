# **Cr0ss-Imp@ct An@lyi of OrdeR Fl0w Imb@l@nc3 (OFI)**

This repository contains code and analysis for performing **Cr0ss-Imp@ct An@lyi** of OrdeR Fl0w Imb@l@nc3 (OFI) in high-frequency equity market data. The goal is to quantify how the OFI of one stock affects the price changes of another stock, both contemporaneously and predictively.

---

## **Folder Structure**
```
project/
├── data/                   # Placeholder for datasets
│   └── order_book_data.csv # Example dataset
├── notebooks/              # Jupyter notebooks for analysis
│   └── ofi_analysis.ipynb  # Main notebook for the task
├── scripts/                # Python scripts for modular implementations
│   ├── data_preparation.py # Script for downloading data from Databento
│   ├── ofi_calculation.py  # Script for OFI calculation
│   ├── pca_integration.py  # Script for PCA integration
│   ├── returns.py          # Script for calculating returns
│   ├── cross_impact.py     # Script for Cr0ss-Imp@ct An@lyi
│   └── visualization.py    # Script for visualization
├── results/                # Outputs (e.g., figures, tables, analysis results)
├── README.md               # Instructions and summary
└── requirements.txt        # List of Python packages
```

---

## **Requirements**
To run the code, you need the following Python packages:
- `pandas`
- `numpy`
- `scikit-learn`
- `seaborn`
- `matplotlib`
- `databento`
- `jupyter notebook`

You can install the required packages using:
```bash
pip install -r requirements.txt
```

---

## **Quick Start**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cross-impact-analysis.git
   cd cross-impact-analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your data to the `data/` folder.

4. Run the Jupyter notebook:
   ```bash
   jupyter notebook notebooks/ofi_analysis.ipynb
   ```

---

## **Data Format**
The dataset should include order book snapshots and trade data with the following columns:
- `symbol`: Stock symbol (e.g., "AAPL").
- `ts_event`: Timestamp of the event (e.g., "2023-10-01 09:30:00").
- `bid_px_00`, `ask_px_00`: Best bid and ask prices.
- `bid_sz_00`, `ask_sz_00`: Best bid and ask sizes.
- Additional columns for deeper levels (e.g., `bid_px_01`, `ask_px_01`, etc.).

Example:
| symbol | ts_event          | bid_px_00 | ask_px_00 | bid_sz_00 | ask_sz_00 | ... |
|--------|-------------------|-----------|-----------|-----------|-----------|-----|
| AAPL   | 2023-10-01 09:30:00| 150.00    | 150.05    | 100       | 200       | ... |
| AAPL   | 2023-10-01 09:30:01| 150.01    | 150.06    | 120       | 180       | ... |

---

## **How to Run the Code**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/cross-impact-analysis.git
   cd cross-impact-analysis
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add Your Data**:
   - Place your high-frequency equity market data in the `data/` folder.
   - Ensure the data includes order book snapshots and trade data with columns like `symbol`, `ts_event`, `bid_px`, `ask_px`, `bid_sz`, `ask_sz`, etc.

4. **Run the Notebook**:
   - Open the `notebooks/ofi_analysis.ipynb` notebook.
   - Execute the cells to perform the analysis.

5. **View Results**:
   - The results (e.g., heatmaps, scatter plots) will be saved in the `results/` folder.

---

## **Code Overview**

### **Scripts**
- **`data_preparation.py`**:
  - Downloads order book and trade data from Databento.

- **`ofi_calculation.py`**:
  - Calculates OrdeR Fl0w Imb@l@nc3 (OFI) at multiple levels of the limit order book.

- **`pca_integration.py`**:
  - Integrates multi-level OFI into a single metric using Principal Component Analysis (PCA).

- **`returns.py`**:
  - Calculates logarithmic returns based on mid-prices.

- **`cross_impact.py`**:
  - Analyzes contemporaneous and predictive cross-impact using LASSO regression.

- **`visualization.py`**:
  - Contains functions for visualizing results (e.g., heatmaps, scatter plots).

### **Notebook**
- **`notebooks/ofi_analysis.ipynb`**:
  - The main notebook that ties everything together.
  - Performs data preprocessing, OFI calculation, PCA integration, Cr0ss-Imp@ct An@lyi, and visualization.

---

## **Analysis Steps**
1. **Data Preprocessing**:
   - Load and clean high-frequency equity market data.
   - Ensure timestamps are in the correct format.

2. **OFI Calculation**:
   - Compute OrdeR Fl0w Imb@l@nc3 (OFI) at multiple levels of the limit order book.

3. **PCA Integration**:
   - Use PCA to integrate multi-level OFI into a single metric.

4. **Logarithmic Returns**:
   - Calculate logarithmic returns based on mid-prices.

5. **Cr0ss-Imp@ct An@lyi**:
   - Analyze contemporaneous cross-impact (OFI at time \( t \) vs. returns at time \( t \)).
   - Analyze predictive cross-impact (OFI at time \( t-1 \) and \( t-5 \) vs. returns at time \( t \)).

6. **Visualization**:
   - Create heatmaps to visualize cross-impact coefficients.
   - Create scatter plots to compare self-impact vs. cross-impact.

---

## **Results**
- **Heatmaps**:
  - Show cross-impact coefficients between stocks.
- **Scatter Plots**:
  - Compare self-impact (within the same stock) vs. cross-impact (between stocks).

---

## **Troubleshooting**
- **Issue**: Missing columns in the dataset.
  - **Solution**: Ensure the dataset includes all required columns (e.g., `symbol`, `ts_event`, `bid_px_00`, `ask_px_00`, etc.).

- **Issue**: Errors during PCA integration.
  - **Solution**: Check for missing or infinite values in the OFI columns.

- **Issue**: Visualization not displaying.
  - **Solution**: Ensure `matplotlib` and `seaborn` are installed and properly configured.

---

## **Future Work**
- Incorporate additional machine learning models (e.g., Random Forest, Gradient Boosting) for Cr0ss-Imp@ct An@lyi.
- Extend the analysis to include more granular time intervals (e.g., milliseconds).
- Add support for additional financial instruments (e.g., futures, options).

---

## **Contributing**
If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contact**
For questions or feedback, please contact:
- **GitHub**: [tqosu](https://github.com/tqosu)

---

### **How to Use**
1. Create the folder structure as shown above.
2. Copy the code for each file into its respective location.
3. Replace the placeholder dataset in `data/order_book_data.csv` with your actual data.
4. Run the `notebooks/ofi_analysis.ipynb` notebook to perform the analysis.
