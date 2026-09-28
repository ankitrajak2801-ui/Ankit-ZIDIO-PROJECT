import streamlit as st
import pandas as pd

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="FORESIGHT Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 FORESIGHT - Demand & Inventory Dashboard")
st.write("Demand Forecast and Inventory Risk Monitoring")


# ==========================================
# LOAD DATA
# ==========================================

forecast = pd.read_csv("data/forecast_results.csv")
risk = pd.read_csv("data/risk_results.csv")
actual = pd.read_csv("data/sales_daily.csv")


# ==========================================
# DATE FORMAT
# ==========================================

forecast["Date"] = pd.to_datetime(forecast["Date"])
risk["Date"] = pd.to_datetime(risk["Date"])
actual["Date"] = pd.to_datetime(actual["Date"])


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🔎 Dashboard Filters")

sku_list = sorted(risk["SKU"].dropna().unique())

selected_sku = st.sidebar.selectbox(
    "Select SKU",
    ["All"] + list(sku_list)
)


# ==========================================
# FILTER
# ==========================================

if selected_sku == "All":

    filtered_risk = risk.copy()
    filtered_forecast = forecast.copy()

else:

    filtered_risk = risk[
        risk["SKU"] == selected_sku
    ].copy()

    filtered_forecast = forecast[
        forecast["SKU"] == selected_sku
    ].copy()


# ==========================================
# SUMMARY
# ==========================================

total_skus = filtered_risk["SKU"].nunique()

high_risk = (
    filtered_risk["risk_level"] == "High"
).sum()

medium_risk = (
    filtered_risk["risk_level"] == "Medium"
).sum()

low_risk = (
    filtered_risk["risk_level"] == "Low"
).sum()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total SKUs", total_skus)

with col2:
    st.metric("🔴 High Risk", high_risk)

with col3:
    st.metric("🟠 Medium Risk", medium_risk)

with col4:
    st.metric("🟢 Low Risk", low_risk)


# ==========================================
# RISK DISTRIBUTION
# ==========================================

st.subheader("🚨 Risk Distribution")

risk_count = filtered_risk["risk_level"].value_counts()

st.bar_chart(risk_count)


# ==========================================
# STOCK VS FORECAST
# ==========================================

st.subheader("📦 Current Stock vs Forecast")

stock_data = filtered_risk[
    [
        "SKU",
        "Predicted_Units",
        "Current_Stock"
    ]
].copy()

stock_data = stock_data.set_index("SKU")

stock_data.columns = [
    "Forecast",
    "Current Stock"
]

st.bar_chart(stock_data)


# ==========================================
# INVENTORY RISK TABLE
# ==========================================

st.subheader("📋 Inventory Risk Analysis")

risk_columns = [
    "Date",
    "SKU",
    "Predicted_Units",
    "Current_Stock",
    "On_Order",
    "Lead_Time_Days",
    "risk_level",
    "recommended_action"
]

st.dataframe(
    filtered_risk[risk_columns],
    width="stretch"
)


# ==========================================
# ACTION REQUIRED
# ==========================================

st.subheader("⚠️ Action Required")

action_data = filtered_risk[
    filtered_risk["risk_level"].isin(
        ["High", "Medium"]
    )
].copy()

if len(action_data) > 0:

    st.dataframe(
        action_data[
            [
                "Date",
                "SKU",
                "Predicted_Units",
                "Current_Stock",
                "risk_level",
                "recommended_action"
            ]
        ],
        width="stretch"
    )

else:

    st.success(
        "No High or Medium risk items found."
    )


# ==========================================
# FORECAST VS ACTUAL
# ==========================================

st.subheader("📈 Forecast vs Actual Sales")

# Weekly actual sales

actual_weekly = (
    actual
    .groupby(
        [
            pd.Grouper(
                key="Date",
                freq="W"
            ),
            "SKU"
        ]
    )["Units_Sold"]
    .sum()
    .reset_index()
)

# Merge actual and forecast

comparison = actual_weekly.merge(
    forecast[
        [
            "Date",
            "SKU",
            "Predicted_Units"
        ]
    ],
    on=["Date", "SKU"],
    how="inner"
)

if selected_sku != "All":

    comparison = comparison[
        comparison["SKU"] == selected_sku
    ]

if len(comparison) > 0:

    chart_data = comparison[
        [
            "Date",
            "Units_Sold",
            "Predicted_Units"
        ]
    ].set_index("Date")

    chart_data.columns = [
        "Actual Sales",
        "Forecast"
    ]

    st.line_chart(chart_data)

else:

    st.warning(
        "Forecast vs Actual data matching nahi mila."
    )


# ==========================================
# DEMAND FORECAST TABLE
# ==========================================

st.subheader("📊 Demand Forecast")

st.dataframe(
    filtered_forecast,
    width="stretch"
)


# ==========================================
# PROJECT INFORMATION
# ==========================================

st.divider()

st.subheader("ℹ️ Project Information")

st.write(
    "FORESIGHT is a Demand & Inventory Intelligence "
    "system designed to monitor demand forecasts, "
    "inventory risk and recommended actions."
)

st.caption(
    "Data Science Project | Python | Pandas | "
    "Scikit-learn | Streamlit"
)