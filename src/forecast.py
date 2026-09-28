import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# ==============================
# 1. LOAD SALES DATA
# ==============================

sales = pd.read_csv("data/sales_daily.csv")

print("Sales data loaded successfully!")


# ==============================
# 2. CONVERT DATE
# ==============================

sales["Date"] = pd.to_datetime(sales["Date"])


# ==============================
# 3. CREATE WEEKLY DATA
# ==============================

weekly = (
    sales
    .groupby([
        pd.Grouper(key="Date", freq="W"),
        "SKU"
    ])["Units_Sold"]
    .sum()
    .reset_index()
)

print("\nWeekly data created successfully!")


# ==============================
# 4. CREATE FEATURES
# ==============================

weekly["week"] = weekly["Date"].dt.isocalendar().week.astype(int)
weekly["month"] = weekly["Date"].dt.month
weekly["year"] = weekly["Date"].dt.year

weekly["lag_1"] = weekly.groupby("SKU")["Units_Sold"].shift(1)
weekly["lag_2"] = weekly.groupby("SKU")["Units_Sold"].shift(2)
weekly["lag_4"] = weekly.groupby("SKU")["Units_Sold"].shift(4)

weekly["rolling_4"] = (
    weekly
    .groupby("SKU")["Units_Sold"]
    .transform(
        lambda x: x.shift(1).rolling(4).mean()
    )
)

weekly = weekly.dropna().reset_index(drop=True)

print("Features created successfully!")


# ==============================
# 5. SELECT FEATURES
# ==============================

features = [
    "week",
    "month",
    "year",
    "lag_1",
    "lag_2",
    "lag_4",
    "rolling_4"
]

X = weekly[features]
y = weekly["Units_Sold"]


# ==============================
# 6. TRAIN / TEST SPLIT
# ==============================

split = int(len(weekly) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

test_data = weekly.iloc[split:].copy()


# ==============================
# 7. TRAIN RANDOM FOREST
# ==============================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("\nRandom Forest model trained successfully!")


# ==============================
# 8. MODEL PREDICTION
# ==============================

predictions = model.predict(X_test)

test_data["Predicted_Units"] = predictions.round(2)


# ==============================
# 9. RANDOM FOREST RESULTS
# ==============================

mae = mean_absolute_error(y_test, predictions)

wape = (
    abs(y_test - predictions).sum()
    / y_test.sum()
) * 100

print("\n===== RANDOM FOREST RESULTS =====")
print("Mean Absolute Error:", round(mae, 2))
print("WAPE:", round(wape, 2), "%")


# ==============================
# 10. SEASONAL NAIVE BASELINE
# ==============================

weekly["Seasonal_Naive"] = (
    weekly.groupby("SKU")["Units_Sold"].shift(4)
)

baseline_data = weekly.iloc[split:].copy()

baseline_data = baseline_data.dropna(
    subset=["Seasonal_Naive"]
)

baseline_wape = (
    abs(
        baseline_data["Units_Sold"]
        - baseline_data["Seasonal_Naive"]
    ).sum()
    /
    baseline_data["Units_Sold"].sum()
) * 100

print("\n===== SEASONAL NAIVE BASELINE =====")
print(
    "Baseline WAPE:",
    round(baseline_wape, 2),
    "%"
)


# ==============================
# 11. MODEL VS BASELINE
# ==============================

print("\n===== MODEL COMPARISON =====")

if wape < baseline_wape:
    print("Random Forest WAPE:", round(wape, 2), "%")
    print("Seasonal Naive WAPE:", round(baseline_wape, 2), "%")
    print("Random Forest has lower WAPE.")
else:
    print("Random Forest WAPE:", round(wape, 2), "%")
    print("Seasonal Naive WAPE:", round(baseline_wape, 2), "%")
    print("Seasonal Naive has lower WAPE.")


# ==============================
# 12. ROLLING-ORIGIN CV
# ==============================

print("\n===== ROLLING-ORIGIN CV =====")

cv_results = []

folds = 3

for fold in range(1, folds + 1):

    train_end = int(
        len(weekly) *
        (0.5 + (fold - 1) * 0.1)
    )

    test_end = int(
        len(weekly) *
        (0.6 + (fold - 1) * 0.1)
    )

    if test_end > len(weekly):
        break

    train_data = weekly.iloc[:train_end]
    test_cv = weekly.iloc[train_end:test_end]

    X_train_cv = train_data[features]
    y_train_cv = train_data["Units_Sold"]

    X_test_cv = test_cv[features]
    y_test_cv = test_cv["Units_Sold"]

    cv_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    cv_model.fit(X_train_cv, y_train_cv)

    cv_predictions = cv_model.predict(X_test_cv)

    cv_wape = (
        abs(
            y_test_cv - cv_predictions
        ).sum()
        /
        y_test_cv.sum()
    ) * 100

    cv_results.append(cv_wape)

    print(
        "Fold",
        fold,
        "WAPE:",
        round(cv_wape, 2),
        "%"
    )


if cv_results:

    average_cv_wape = sum(cv_results) / len(cv_results)

    print(
        "\nAverage Rolling CV WAPE:",
        round(average_cv_wape, 2),
        "%"
    )


# ==============================
# 13. FORECAST SAMPLE
# ==============================

print("\n===== FORECAST SAMPLE =====")

print(
    test_data[
        [
            "Date",
            "SKU",
            "Units_Sold",
            "Predicted_Units"
        ]
    ].tail(10)
)


# ==============================
# 14. SAVE FORECAST FILE
# ==============================

forecast_results = test_data[
    [
        "Date",
        "SKU",
        "Units_Sold",
        "Predicted_Units"
    ]
]

forecast_results.to_csv(
    "data/forecast_results.csv",
    index=False
)


print("\n==============================")
print("FORECAST FILE SAVED")
print("==============================")
print("Saved as: data/forecast_results.csv")