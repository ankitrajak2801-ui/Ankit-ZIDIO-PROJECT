import pandas as pd

# ==========================================
# 1. LOAD FILES
# ==========================================

forecast = pd.read_csv("data/forecast_results.csv")
inventory = pd.read_csv("data/inventory_snapshots.csv")
sku_master = pd.read_csv("data/sku_master.csv")


# ==========================================
# 2. DATE CONVERSION
# ==========================================

forecast["Date"] = pd.to_datetime(forecast["Date"])

inventory["Snapshot_Date"] = pd.to_datetime(
    inventory["Snapshot_Date"]
)


# ==========================================
# 3. CREATE MONTH COLUMN
# ==========================================

forecast["Month"] = forecast["Date"].dt.to_period("M")

inventory["Month"] = (
    inventory["Snapshot_Date"].dt.to_period("M")
)


# ==========================================
# 4. MERGE FORECAST + INVENTORY
# ==========================================

risk = forecast.merge(
    inventory,
    on=["Month", "SKU"],
    how="left"
)


# ==========================================
# 5. MERGE SKU MASTER
# ==========================================

if "Unit_Cost" in sku_master.columns:

    risk = risk.merge(
        sku_master[["SKU", "Unit_Cost"]],
        on="SKU",
        how="left"
    )

else:

    risk["Unit_Cost"] = 0


# ==========================================
# 6. CHECK INVENTORY DATA
# ==========================================

risk["Inventory_Available"] = (
    risk["Current_Stock"].notna()
)


# ==========================================
# 7. AVAILABLE STOCK
# ==========================================

risk["available_stock"] = (
    risk["Current_Stock"].fillna(0)
    + risk["On_Order"].fillna(0)
)


# ==========================================
# 8. LEAD-TIME DEMAND
# ==========================================

risk["Lead_Time_Demand"] = (
    risk["Predicted_Units"]
    * risk["Lead_Time_Days"].fillna(7)
    / 7
)


# ==========================================
# 9. STOCKOUT RISK
# ==========================================

risk["stockout_risk"] = (
    risk["Lead_Time_Demand"]
    > risk["available_stock"]
)

risk.loc[
    ~risk["Inventory_Available"],
    "stockout_risk"
] = False


# ==========================================
# 10. OVERSTOCK RISK
# ==========================================

risk["overstock_risk"] = (
    risk["Current_Stock"]
    > risk["Predicted_Units"] * 2
)

risk.loc[
    ~risk["Inventory_Available"],
    "overstock_risk"
] = False


# ==========================================
# 11. REORDER QUANTITY
# ==========================================

risk["Reorder_Quantity"] = (
    risk["Lead_Time_Demand"]
    - risk["available_stock"]
).clip(lower=0)


# ==========================================
# 12. OVERSTOCK QUANTITY
# ==========================================

risk["Overstock_Quantity"] = (
    risk["Current_Stock"]
    - risk["Predicted_Units"]
).clip(lower=0)


# ==========================================
# 13. REORDER VALUE
# ==========================================

risk["Reorder_Value"] = (
    risk["Reorder_Quantity"]
    * risk["Unit_Cost"].fillna(0)
)


# ==========================================
# 14. OVERSTOCK VALUE
# ==========================================

risk["Overstock_Value"] = (
    risk["Overstock_Quantity"]
    * risk["Unit_Cost"].fillna(0)
)


# ==========================================
# 15. RISK LEVEL
# ==========================================

def get_risk_level(row):

    if not row["Inventory_Available"]:
        return "No Inventory Data"

    elif row["stockout_risk"]:
        return "High"

    elif row["overstock_risk"]:
        return "Medium"

    else:
        return "Low"


risk["risk_level"] = risk.apply(
    get_risk_level,
    axis=1
)


# ==========================================
# 16. RECOMMENDED ACTION
# ==========================================

def get_action(row):

    if not row["Inventory_Available"]:
        return "No Inventory Data"

    elif row["stockout_risk"]:
        return "Reorder"

    elif row["overstock_risk"]:
        return "Markdown"

    else:
        return "Monitor"


risk["recommended_action"] = risk.apply(
    get_action,
    axis=1
)


# ==========================================
# 17. RISK VALUE
# ==========================================

risk["Risk_Value"] = 0.0

risk.loc[
    risk["recommended_action"] == "Reorder",
    "Risk_Value"
] = risk["Reorder_Value"]

risk.loc[
    risk["recommended_action"] == "Markdown",
    "Risk_Value"
] = risk["Overstock_Value"]


# ==========================================
# 18. SAVE RESULT
# ==========================================

risk.to_csv(
    "data/risk_results.csv",
    index=False
)


# ==========================================
# 19. DISPLAY RESULT
# ==========================================

print("\n===== RISK SCORING COMPLETE =====")

print(
    risk[
        [
            "Date",
            "SKU",
            "Predicted_Units",
            "Current_Stock",
            "Lead_Time_Days",
            "Reorder_Quantity",
            "Risk_Value",
            "risk_level",
            "recommended_action"
        ]
    ].head(10)
)

print("\nRisk Level Summary:")
print(risk["risk_level"].value_counts())

print("\nRisk file saved successfully!")
print("Location: data/risk_results.csv")