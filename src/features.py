def create_features(df):
    df = df.sort_values(["Store", "Date"])

    # Time features
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)

    # Lag features
    df["Sales_lag_1"] = df.groupby("Store")["Sales"].shift(1)
    df["Sales_lag_7"] = df.groupby("Store")["Sales"].shift(7)

    # Rolling features
    df["Rolling_mean_7"] = (
        df.groupby("Store")["Sales"]
        .shift(1)
        .rolling(window=7)
        .mean()
    )

    # Drop NA created by lag
    df = df.dropna()

    return df