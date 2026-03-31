from fastapi import FastAPI
from src.predict import make_prediction

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Demand Forecast API Running"}


@app.post("/predict")
def predict(data: dict):
    preds, action = make_prediction(data)

    return {
        "predictions": preds,
        "next_day_prediction": preds[0],
        "recommendation": action
    }