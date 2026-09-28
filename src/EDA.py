
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load sales data
sales = pd.read_csv("data/sales_daily.csv")

# 2. Convert Date column
sales["Date"] = pd.to_datetime(sales["Date"])

# 3. Daily total sales
daily_sales = sales.groupby("Date")["Units_Sold"].sum()

# 4. Daily Sales Trend Chart
plt.figure(figsize=(12, 6))
plt.plot(daily_sales.index, daily_sales.values)

plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Units Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Top 10 Selling SKUs
top_skus = (
    sales.groupby("SKU")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# 6. Top 10 SKUs Chart
plt.figure(figsize=(10, 6))
top_skus.plot(kind="bar")

plt.title("Top 10 Selling SKUs")
plt.xlabel("SKU")
plt.ylabel("Total Units Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 7. Monthly Sales
monthly_sales = (
    sales.groupby(sales["Date"].dt.to_period("M"))["Units_Sold"]
    .sum()
)

# 8. Monthly Sales Chart
plt.figure(figsize=(12, 6))
monthly_sales.plot(kind="bar")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Units Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 9. Basic Business Insights

print("\n===== BUSINESS INSIGHTS =====")

# Highest selling SKU
best_sku = (
    sales.groupby("SKU")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
    .head(1)
)

print("\n1. Highest Selling SKU:")
print(best_sku)

# Lowest selling SKU
low_sku = (
    sales.groupby("SKU")["Units_Sold"]
    .sum()
    .sort_values()
    .head(1)
)

print("\n2. Lowest Selling SKU:")
print(low_sku)

# Highest sales month
best_month = (
    sales.groupby(sales["Date"].dt.to_period("M"))["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
    .head(1)
)

print("\n3. Highest Selling Month:")
print(best_month)