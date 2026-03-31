import joblib
import pandas as pd
from src.decision import recommend

# Load model
model = joblib.load("models/model.pkl")
feature_names = joblib.load("models/features.pkl")


def make_prediction(input_data):

    df = pd.DataFrame([input_data])

    # Ensure all features exist
    for col in feature_names:
        if col not in df:
            df[col] = 0

    df = df[feature_names]

    # -------- MULTI-STEP PREDICTION --------
    preds = model.predict(df)[0]

    # -------- DECISION --------
    action = recommend(preds[0])

    return preds.tolist(), action