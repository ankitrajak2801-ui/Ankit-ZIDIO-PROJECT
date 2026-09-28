import pandas as pd

print("FORESIGHT PROJECT STARTED")

sales = pd.read_csv("data/sales_daily.csv")
sku = pd.read_csv("data/sku_master.csv")
calendar = pd.read_csv("data/calendar.csv")

print("\nSales Data:")
print(sales.head())

print("\nSKU Data:")
print(sku.head())

print("\nCalendar Data:")
print(calendar.head())

# Naya code yahan neeche add karna hai
print("\n--- DATA QUALITY CHECK ---")

print("Sales rows and columns:", sales.shape)
print("SKU rows and columns:", sku.shape)
print("Calendar rows and columns:", calendar.shape)

print("\nSales columns:")
print(sales.columns.tolist())

print("\nSKU columns:")
print(sku.columns.tolist())

print("\nCalendar columns:")
print(calendar.columns.tolist())

print("\nMissing values in Sales:")
print(sales.isnull().sum())
print("\n--- DATA CLEANING CHECK ---")

# Duplicate rows check
print("Sales duplicate rows:", sales.duplicated().sum())
print("SKU duplicate rows:", sku.duplicated().sum())
print("Calendar duplicate rows:", calendar.duplicated().sum())

# Data types check
print("\nSales Data Types:")
print(sales.dtypes)

print("\nSKU Data Types:")
print(sku.dtypes)

print("\nCalendar Data Types:")
print(calendar.dtypes)

print("Sales duplicates:", sales.duplicated().sum())
print("SKU duplicates:", sku.duplicated().sum())
print("Calendar duplicates:", calendar.duplicated().sum())

print("\n--- DATE CHECK ---")

print("Sales date type:", sales["Date"].dtype)
print("Calendar date type:", calendar["date"].dtype)

print("\nSales first date:", sales["Date"].min())
print("Sales last date:", sales["Date"].max())

print("\n--- DATE CONVERSION ---")

sales["Date"] = pd.to_datetime(sales["Date"])
calendar["date"] = pd.to_datetime(calendar["date"])

print("Sales date type after conversion:", sales["Date"].dtype)
print("Calendar date type after conversion:", calendar["date"].dtype)

print("\n--- MERGING DATA ---")

# Sales + Calendar ko Date ke basis par join karna
df = sales.merge(
    calendar,
    left_on="Date",
    right_on="date",
    how="left"
)

print("Final dataset shape:", df.shape)

print("\nFinal dataset columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\n--- SKU DATA MERGE ---")

df = df.merge(
    sku,
    on="SKU",
    how="left"
)

print("Final dataset shape after SKU merge:", df.shape)

print("\nFinal columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\n--- FINAL DATA QUALITY CHECK ---")

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\n--- DATA CLEANING ---")

# Missing values ko check karke fill karna
df = df.ffill()

print("Missing values after cleaning:")
print(df.isnull().sum())

print("\nFinal dataset shape:")
print(df.shape)

print("\n--- BASIC EDA ---")

print("\nTotal Sales Units:")
print(df["Units_Sold"].sum())

print("\nTotal Revenue:")
print(df["Revenue"].sum())

print("\nAverage Daily Units Sold:")
print(df["Units_Sold"].mean())

print("\nTop 10 SKUs by Units Sold:")
print(
    df.groupby("SKU")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)