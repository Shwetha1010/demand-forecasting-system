import pandas as pd

def load_and_preprocess():
    # Load data
    train = pd.read_csv("data/train.csv", low_memory=False)
    store = pd.read_csv("data/store.csv")

    # Merge
    df = train.merge(store, on="Store", how="left")

    # Remove closed stores
    df = df[df["Open"] != 0]

    # Convert date
    df["Date"] = pd.to_datetime(df["Date"])

    # Fill missing values
    df["CompetitionDistance"] = df["CompetitionDistance"].fillna(
        df["CompetitionDistance"].median()
    )

    # 🔥 Fix StateHoliday
    df["StateHoliday"] = df["StateHoliday"].astype(str)
    df["StateHoliday"] = df["StateHoliday"].replace({
        "0": 0,
        "a": 1,
        "b": 2,
        "c": 3
    }).astype(int)

    # 🔥 Fix PromoInterval
    df["PromoInterval"] = df["PromoInterval"].fillna("None")
    df["PromoInterval"] = df["PromoInterval"].apply(
        lambda x: len(x.split(",")) if x != "None" else 0
    )

    # Encode categorical
    for col in ["StoreType", "Assortment"]:
        df[col] = df[col].astype("category").cat.codes

    return df