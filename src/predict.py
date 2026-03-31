import joblib
import pandas as pd
import numpy as np
from src.decision import recommend

model = joblib.load("models/model.pkl")
feature_names = joblib.load("models/features.pkl")


def forecast_next_7_days(input_data):
    predictions = []
    temp_data = input_data.copy()

    for i in range(7):
        df = pd.DataFrame([temp_data])

        # Ensure all features exist
        for col in feature_names:
            if col not in df:
                df[col] = 0

        df = df[feature_names]

        pred = model.predict(df)[0]
        predictions.append(pred)

        # Update lag features (IMPORTANT)
        temp_data["Sales_lag_7"] = temp_data["Sales_lag_1"]
        temp_data["Sales_lag_1"] = pred

        # Rolling smoothing
        temp_data["Rolling_mean_7"] = np.mean(
            [temp_data["Sales_lag_1"], temp_data["Sales_lag_7"], pred]
        )

    return predictions


def make_prediction(input_data):
    preds = forecast_next_7_days(input_data)

    # Smooth predictions (IMPORTANT FIX)
    preds_smooth = pd.Series(preds).rolling(2, min_periods=1).mean().tolist()

    action = recommend(preds_smooth[0])

    return preds_smooth, action