import pandas as pd

def create_features(df):

    # -------- DATE FEATURES --------
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)

    # -------- LAG FEATURES --------
    df = df.sort_values(["Store", "Date"])

    df["Sales_lag_1"] = df.groupby("Store")["Sales"].shift(1)
    df["Sales_lag_7"] = df.groupby("Store")["Sales"].shift(7)

    # -------- ROLLING --------
    df["Rolling_mean_7"] = df.groupby("Store")["Sales"].shift(1).rolling(7).mean()

    # -------- TARGET (MULTI-STEP) --------
    for i in range(1, 8):
        df[f"y{i}"] = df.groupby("Store")["Sales"].shift(-i)

    # -------- DROP NA --------
    df = df.dropna()

    return df