from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import make_prediction

app = FastAPI(title="Demand Forecast API")


# ------------------- INPUT SCHEMA (IMPORTANT) -------------------
class InputData(BaseModel):
    Store: int
    Promo: int
    DayOfWeek: int
    Sales_lag_1: float
    Sales_lag_7: float
    Rolling_mean_7: float
    Year: int
    Month: int
    Day: int
    WeekOfYear: int
    StateHoliday: int
    SchoolHoliday: int
    StoreType: int
    Assortment: int
    CompetitionDistance: float
    PromoInterval: int


# ------------------- HOME ROUTE -------------------
@app.get("/")
def home():
    return {"message": "✅ Demand Forecast API is running"}


# ------------------- PREDICT ROUTE -------------------
@app.post("/predict")
def predict(data: InputData):
    # Convert Pydantic model to dictionary
    input_dict = data.dict()

    preds, action = make_prediction(input_dict)

    return {
        "predictions": preds,
        "next_day_prediction": preds[0],
        "recommendation": action
    }