# FORESIGHT - Demand & Inventory Intelligence

## Project Overview

FORESIGHT is a Data Science project for demand forecasting and inventory risk monitoring.

The project uses historical sales and inventory data to:

- Forecast future product demand
- Identify stockout risk
- Identify overstock risk
- Provide recommended inventory actions
- Display results through a Streamlit dashboard

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Streamlit

## Project Structure

```text
Ankit-ZIDIO-PROJECT/
│
├── app/
│   └── app.py
│
├── data/
│   ├── sales_daily.csv
│   ├── sku_master.csv
│   ├── calendar.csv
│   ├── inventory_snapshots.csv
│   ├── forecast_results.csv
│   └── risk_results.csv
│
├── notebooks/
│
├── src/
│   ├── main.py
│   ├── EDA.py
│   ├── forecast.py
│   └── risk.py
│
├── requirements.txt
└── README.md