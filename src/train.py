import joblib
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from preprocess import load_and_preprocess
from features import create_features


def main():
    # Load + preprocess
    df = load_and_preprocess()

    # Feature engineering
    df = create_features(df)

    # Split features & target
    X = df.drop(["Sales", "Date"], axis=1)
    y = df["Sales"]

    # Train-test split (time-aware)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # Model
    model = LGBMRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=-1,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predictions
    preds = model.predict(X_test)

    # Evaluation

    rmse = mean_squared_error(y_test, preds) ** 0.5   
    print(f"RMSE: {rmse:.2f}")

    # Save model
    joblib.dump(X.columns.tolist(), "models/features.pkl")
    print("Model saved successfully!")


if __name__ == "__main__":
    main()