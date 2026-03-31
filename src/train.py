import joblib
import os
from lightgbm import LGBMRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split

from preprocess import load_and_preprocess
from features import create_features


def main():

    df = load_and_preprocess()
    df = create_features(df)

    # -------- FEATURES --------
    target_cols = [f"y{i}" for i in range(1, 8)]

    X = df.drop(["Sales", "Date"] + target_cols, axis=1)
    y = df[target_cols]

    # -------- SPLIT --------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # -------- MODEL --------
    model = MultiOutputRegressor(LGBMRegressor(n_estimators=200))
    model.fit(X_train, y_train)

    # -------- SAVE --------
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/model.pkl")
    joblib.dump(list(X.columns), "models/features.pkl")

    print("Model trained and saved successfully!")


if __name__ == "__main__":
    main()